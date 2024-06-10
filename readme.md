
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt
django-admin startproject text_detection_project
cd text_detection_project
django-admin startapp text_detection_app
