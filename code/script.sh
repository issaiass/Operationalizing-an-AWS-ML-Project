echo "[INFO] - Downloading Dataset START"
wget https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip
echo "[INFO] - Downloading Dataset FINISH"
echo "[INFO] - Unziping Dataset START"
unzip dogImages.zip
echo "[INFO] - Unzip Dataset FINISH"
echo "[INFO] - Creating Directory TrainedModels"
mkdir TrainedModels
echo "[INFO] - Training START"
python solution.py
echo "[INFO] - Training Finish"