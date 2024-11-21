from __future__ import annotations
import bentoml
from bentoml.io import Image as BentoImage, JSON
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import base64
import io

# Определяем сервис
svc = bentoml.Service("bee_wasp_classifier_service")

# Загружаем ONNX модель при инициализации сервиса
session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

@svc.api(input=BentoImage(), output=JSON())
def predict(input_image) -> dict:
    """
    Выполнение инференса модели и возврат изображения с детекцией.
    Args:
        input_image: Входное изображение.
    Returns:
        dict: Изображение с детекцией, закодированное в base64.
    """
    # Предобработка данных
    image = input_image.convert("RGB")
    image_resized = image.resize((640, 640))

    # Сохраняем копию изображения для рисования bounding box-ов
    draw_image = image_resized.copy()

    # Преобразование изображения в массив
    image_array = np.asarray(image_resized).astype(np.float32)
    image_array = np.transpose(image_array, (2, 0, 1))  # Преобразование в формат CHW
    image_array = np.expand_dims(image_array, axis=0) / 255.0  # Нормализация

    # Выполнение инференса
    predictions = session.run([output_name], {input_name: image_array})

    # Постобработка и рисование bounding box-ов
    result_image = postprocess(predictions, draw_image)

    # Конвертация изображения в base64
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": img_str}

def postprocess(predictions, image):
    """
    Постобработка выходных данных модели и рисование bounding box-ов.
    Args:
        predictions (list): Сырые выходные данные модели.
        image (PIL Image): Изображение для рисования bounding box-ов.
    Returns:
        PIL Image: Изображение с нарисованными bounding box-ами.
    """
    # Получаем предсказания
    predictions = predictions[0][0]  # Предполагаем батч размером 1

    if predictions.size == 0:
        return image  # Нет предсказаний

    # Отфильтруем предсказания по порогу уверенности
    conf_threshold = 0.25
    predictions = predictions[predictions[:, 4] >= conf_threshold]

    if predictions.size == 0:
        return image  # Нет предсказаний выше порога

    # Имена классов
    class_names = ['bee', 'wasp']

    # Рисование bounding box-ов на изображении
    draw = ImageDraw.Draw(image)

    for pred in predictions:
        x1, y1, x2, y2, conf, class_id = pred[:6]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        class_id = int(class_id)
        label = f"{class_names[class_id]}: {conf:.2f}"

        # Рисуем bounding box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        # Рисуем текст
        draw.text((x1, y1 - 10), label, fill="red")

    return image
