# SSH doesn't support wayland forwarding, so must have a X server installed
# On client machine
ssh -Y drow@192.168.10.62
cd /home/drow/projects/ppocr-v5-fine-tune
source .venv/bin/activate
QT_QPA_PLATFORM=xcb PPOCRLabel --lang=english
open /ppocr-labeled-data for annotating the data

# On server
Ensure that in the ssh config file, x11 forwarding = yes
if not set it to yes and restart ssh server

# When labeling
Look through:
https://paddlepaddle.github.io/PaddleX/latest/en/data_annotations/ocr_modules/text_detection_recognition.html
to understand PPOCRLabel shortcuts etc
Make sure the labeling is correct and unique samples are pioritied.
Make sure all text in the PDF is labeled, not only the ones you want to improve.

# After labeling with PPOCRLabel
python .venv/lib64/python3.12/site-packages/PPOCRLabel/gen_ocr_train_val_test.py \
  --datasetRootPath ./ppocr-labeled-data \
  --detRootPath ./train_data/det \
  --recRootPath ./train_data/rec \
  --trainValTestRatio 6:2:2