DATASET_NAME="andrewmvd/wholesome-images"
ZIP_DATASET="./wholesome-images.zip"
DATASET_DIR="./wholesome-images"

if ! [[ -d $DATASET_DIR ]] ; then
  if ! [[ -f $ZIP_DATASET ]]; then
    kaggle datasets download $DATASET_NAME
    echo "Successfully loaded zip dataset"
  fi

  unzip -q $ZIP_DATASET -d $DATASET_DIR
  echo "Extracted images"

  rm $ZIP_DATASET
fi


