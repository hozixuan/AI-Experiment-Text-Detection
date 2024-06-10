# text_detection_app/views.py

import io
from ninja import Router, File, UploadedFile
from django.http import HttpRequest, HttpResponse
from PIL import Image, ImageDraw
import easyocr
from typing import List
import logging


logger = logging.getLogger(__name__)

reader = easyocr.Reader(["en"], gpu=False)

router = Router()


@router.post("/detect_text")
def detect_text(request: HttpRequest, file: UploadedFile = File(...)):
    try:
        image_byte = file.read()
        results = reader.readtext(image_byte)
        print(f"{results=}")
        texts = [result[1] for result in results]
        return {"texts": texts}
    except Exception as e:
        logger.error(f"Error detecting text: {e}")
        return {"error": str(e)}, 500


@router.post("/detect_and_draw_text")
def detect_and_draw_text(
    request: HttpRequest,
    file: UploadedFile = File(...),
) -> HttpResponse:
    try:
        image_byte = file.read()
        img = Image.open(io.BytesIO(image_byte))
        results = reader.readtext(image_byte)

        draw = ImageDraw.Draw(img)
        for result in results:
            top_left = tuple(result[0][0])
            bottom_right = tuple(result[0][2])
            draw.rectangle([top_left, bottom_right], outline="red", width=2)
            draw.text(top_left, result[1], fill="red")

        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)

        return HttpResponse(output, content_type="image/png")
    except Exception as e:
        logger.error(f"Error detecting and drawing text: {e}")
        return HttpResponse({"error": str(e)}, status=500)


# text_detection_app/views.py

from django.shortcuts import render


@router.get("/web")
def get_detect_text(request):
    return render(request, "index.html")
