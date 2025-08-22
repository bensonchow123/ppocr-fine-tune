# PaddleOCR Fine-tuning recognition module documentation

Customised documentation for fine tuning the recognition module on the 3x 5080 server.
## Reference Documentation

**Fine tune docs:**  
http://www.paddleocr.ai/main/en/version3.x/module_usage/text_recognition.html#4-secondary-development

**Prepare dataset docs:**  
https://paddlepaddle.github.io/PaddleX/latest/en/data_annotations/ocr_modules/text_detection_recognition.html#3-data-format

## 4.1 Dataset and Pre-trained Model Preparation

### 4.1.1 Dataset Preparation

**Use PPOCRLabel for labeling:**  
https://github.com/PFCCLab/PPOCRLabel

Hightlight poorly recognised words and the labeling program will crop it  
Then manually annotate the poorly recognised words

The program will create a:
- `/crop_img` directory
- `fileState.txt`
- `Label.txt`
- `rec_gt.txt`

Modify the data generated to match the example dataset below:  
https://paddle-model-ecology.bj.bcebos.com/paddlex/data/ocr_rec_dataset_examples.tar  
according to the prepare dataset docs at the start of the file.

### 4.1.2 Download the pre-trained model

Depend on the package manager for the 3x 5080 machine, install the wget package

```bash
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained.pdparams
```

## 4.2 Model Training
### 4.2.1 Training preparation
Download the yaml configureration file for the PP-OCRv5_server_rec recognition model:  
https://github.com/PaddlePaddle/PaddleOCR/blob/main/configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml

Edit the yml file point to the dataset created.

### 4.2.2 Begin training

Git clone the ppocr repo  
Run the command below, cause we have 3 GPUs:

```bash
python3 -m paddle.distributed.launch --gpus '0,1,2'  tools/train.py -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml -o Global.pretrained_model=./PP-OCRv5_server_rec_pretrained.pdparams
```

## 4.3 Model Evaluation

```bash
python3 tools/eval.py -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml -o \
Global.pretrained_model=output/xxx/xxx.pdparams
```

## 4.4 Model Export

```bash
python3 tools/export_model.py -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml -o \
Global.pretrained_model=output/xxx/xxx.pdparams \
Global.save_inference_dir="./PP-OCRv5_server_rec_infer/"
```

After exporting the model, the static graph model will be stored in `./PP-OCRv5_server_rec_infer/` in the current directory. In this directory, you will see the following files:

```
./PP-OCRv5_server_rec_infer/
├── inference.json
├── inference.pdiparams
├── inference.yml
```

At this point, the secondary development is complete. This static graph model can be directly integrated into the PaddleOCR API.

Used like this:

```python
ocr = PaddleOCR(
    text_recognition_model_dir='path/to/your/fine_tuned_rec_model',
    lang='en'
)
```
