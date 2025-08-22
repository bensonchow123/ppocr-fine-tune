# create training dataset
use data-annotation-notes.md

# Created and activate virtual environement
python -m venv .venv  
source .venv/bin/activate  
  
# checked that the cuda version is 12.6  
python -m pip install --pre paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/nightly/cu126/ 

# saw setuptools not installed in venv  
pip install setuptools  
  
# ran python test.py, paddle reports well on one gpu but not one 3 gpus, the error:
PaddlePaddle works well on 1 GPU.  
[2025-08-06 15:19:58,671] [ WARNING] install_check.py:289 - PaddlePaddle meets some problem with 3 GPUs. This may be caused by:  
 1. There is not enough GPUs visible on your system  
 2. Some GPUs are occupied by other process now  
 3. NVIDIA-NCCL2 is not installed correctly on your system. Please follow instruction on https://github.com/NVIDIA/nccl-tests  
 to test your NCCL, or reinstall it following https://docs.nvidia.com/deeplearning/sdk/nccl-install-guide/index.html  
Solved by insalled NCCL

# Installed paddleocr
pip install paddleocr

# Downloaded the pretrained regcognisation (rec) model, moved to finetunning-misc
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained.pdparams

# Downloaded the yaml configureration file for the PP-OCRv5_server_rec recognition model, moved to finetunning-misc:  
wget https://github.com/PaddlePaddle/PaddleOCR/blob/main/configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml

# realised that the yaml file downloaded is corrupted, fixed it with:
rm finetuning-misc/PP-OCRv5_server_rec.yml
wget -O finetuning-misc/PP-OCRv5_server_rec.yml \
  https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/main/configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml

# git clone the ppocr repo for the finetuning tools
git clone https://github.com/PaddlePaddle/PaddleOCR.git

# install training script requirements
pip install -r PaddleOCR/requirements.txt

# began training
tmux new-session -d -s ppocr-training
tmux attach-session -t ppocr-training
cd /home/drow/projects/ppocr-v5-fine-tune
source .venv/bin/activate
cd PaddleOCR
python3 -m paddle.distributed.launch --gpus '0,1,2'  tools/train.py -c ../finetuning-misc/PP-OCRv5_server_rec.yml -o Global.pretrained_model=../finetuning-misc/PP-OCRv5_server_rec_pretrained.pdparams
Detach from session: Press Ctrl+b then d
Reattach from session: tmux attach-session -t ppocr-training

# Take the best weights (usally highest epoch)?
Edit the epoch number
python3 tools/export_model.py -c ../finetuning-misc/PP-OCRv5_server_rec.yml -o \
Global.checkpoints=./output/PP-OCRv5_server_rec/iter_epoch_xx \ 
Global.save_inference_dir=./PP-OCRv5_server_rec_infer

# test the model created
run python paddle-model-test.py