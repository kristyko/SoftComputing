import os
import csv
import numpy as np

from mpi4py import MPI
from subprocess import call
from PIL import Image


DATASET_NAME = "wholesome-images"
ORIG_IMG_DIR = f"./{DATASET_NAME}/images"
DATA_CSV = f"./{DATASET_NAME}/aww_dataset.csv"
PROCESSED_IMG_DIR = f"./{DATASET_NAME}_processed/images-"

IMG_SIZE = 64

comm = MPI.COMM_WORLD
SIZE, RANK = comm.Get_size(), comm.Get_rank()


def load_dataset():
    with open("./load_dataset.sh", 'rb') as file:
        script = file.read()
    rc = call(script, shell=True)


def resize_img(img_name, new_dir, size=IMG_SIZE):
    img = Image.open(os.path.join(ORIG_IMG_DIR, img_name))
    processed_img = img.resize((size, size))
    # processed_img.save(os.path.join(new_dir, img_name))


def main():
    load_dataset()
    new_dir = f"{PROCESSED_IMG_DIR}{SIZE}"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir, exist_ok=True)
    dataset = []
    if RANK == 0:
        with open(DATA_CSV, "r") as data_file:
            data = csv.DictReader(data_file)
            dataset = np.array_split([row["filename"] for row in data], SIZE)
    comm.Barrier()
    start = MPI.Wtime()
    dataset = comm.scatter(dataset, root=0)
    for img_path in dataset:
        resize_img(img_path, new_dir)
    comm.Barrier()
    end = MPI.Wtime()
    if RANK == 0:
        with open("results.txt", "a") as output:
            output.write(f"n:{SIZE} time:{end - start}\n")


if __name__ == "__main__":
    main()
