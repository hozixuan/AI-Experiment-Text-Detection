# text_detection_app/views.py

from ninja import Router, File, UploadedFile
from django.http import HttpRequest
import easyocr
from typing import List
import logging


logger = logging.getLogger(__name__)

reader = easyocr.Reader(["en"], gpu=False)

router = Router()


@router.post("/detect_text")
def detect_text(request: HttpRequest, file: UploadedFile = File(...)):
    try:
        image = file.read()
        results = reader.readtext(image)
        print(f"{results=}")
        texts = [result[1] for result in results]
        return {"texts": texts}
    except Exception as e:
        logger.error(f"Error detecting text: {e}")
        return {"error": str(e)}, 500


# text_detection_app/views.py

from django.shortcuts import render


@router.get("/detect_text")
def get_detect_text(request):
    return render(request, "index.html")
