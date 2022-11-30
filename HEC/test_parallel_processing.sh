for N in {1..10}
do
  mpiexec -n $N python process_images_parallel.py
done