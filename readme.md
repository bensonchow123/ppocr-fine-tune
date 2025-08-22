# PP-OCRv5 Fine-Tune
The actual code is at the company server at /drow//projects/ppocr-v5-fine-tune, the training data is avaliable there.

## 1. Create Training Dataset
- Go to `data-annotation-notes` to run PPOCRLabel on the server to label training data.
- Requires an X server installed on your PC
- The labeling program can be ran on your PC instead, but it is extremely slow if you don't have a PC with > 8GB of vram and > 10GB of ram and be able to run paddle paddle in GPU mode, which uses CUDA.

## 2. Train the Model
Using all 3 GPUs, remember to test GPU load with nvidia-smi
Paste the following one by one
```bash
tmux new-session -d -s ppocr-training
tmux attach-session -t ppocr-training
cd /home/drow/projects/ppocr-v5-fine-tune
source .venv/bin/activate
cd PaddleOCR
python3 -m paddle.distributed.launch --gpus '0,1,2' tools/train.py \
  -c ../finetuning-misc/PP-OCRv5_server_rec.yml \
  -o Global.pretrained_model=../finetuning-misc/PP-OCRv5_server_rec_pretrained.pdparams
```

tmux detach: Ctrl+b then d  
tmux reattach:
```bash
tmux attach-session -t ppocr-training
```

## 3. Evaluate / Export Model
Select the best epoch (replace `iter_epoch_xx`):
```bash
python3 tools/export_model.py \
  -c ../finetuning-misc/PP-OCRv5_server_rec.yml \
  -o Global.checkpoints=./output/PP-OCRv5_server_rec/iter_epoch_xx \
     Global.save_inference_dir=./PP-OCRv5_server_rec_infer
```

## 4. Test the Fine-Tuned Model
```bash
cd /home/drow/projects/ppocr-v5-fine-tune
python paddle-model-test.py
```