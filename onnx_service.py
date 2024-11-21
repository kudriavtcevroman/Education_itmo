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

# Загружаем модель при инициализации сервиса
session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

@svc.api(input=BentoImage(), output=JSON())
def predict(input_image: Image.Image) -> dict:
    # Предобработка данных
    image = input_image.convert("RGB")
    image_resized = image.resize((256, 256))
    draw_image = image_resized.copy()

    # Преобразование изображения в массив
    image_array = np.asarray(image_resized).astype(np.float32)
    image_array = image_array[:, :, ::-1]  # Перестановка каналов RGB -> BGR
    image_array = np.transpose(image_array, (2, 0, 1))
    image_array = np.expand_dims(image_array, axis=0) / 255.0

    # Выполнение инференса
    predictions = session.run([output_name], {input_name: image_array})

    # Постобработка и рисование bounding box-ов
    result_image, detected_classes = postprocess(predictions, draw_image)

    # Конвертация изображения в base64
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": img_str, "detected_classes": detected_classes}

def postprocess(predictions, image):
    # Предположим, что predictions[0] имеет форму [num_predictions, 85]
    # Где первые 4 элемента - координаты бокса, 5-й - уверенность, остальные 80 - вероятности классов
    predictions = predictions[0]  # Извлекаем предсказания

    if predictions.size == 0:
        return image, []  # Нет предсказаний

    # Порог уверенности для бокса
    conf_threshold = 0.25
    # Порог для вероятности класса
    class_conf_threshold = 0.25

    boxes = []
    detected_classes = []

    for pred in predictions:
        # Извлекаем уверенность объекта
        obj_conf = pred[4]

        if obj_conf < conf_threshold:
            continue  # Пропускаем, если уверенность ниже порога

        # Извлекаем вероятности классов
        class_probs = pred[5:]
        class_id = np.argmax(class_probs)
        class_conf = class_probs[class_id]

        if class_conf < class_conf_threshold:
            continue  # Пропускаем, если уверенность в классе ниже порога

        # Общая уверенность - произведение уверенности объекта и класса
        conf = obj_conf * class_conf

        # Извлекаем координаты бокса
        x1, y1, x2, y2 = pred[:4]

        # Масштабируем координаты
        width, height = image.size
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height

        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Добавляем данные в списки
        boxes.append([x1, y1, x2, y2, conf, class_id])
        detected_classes.append(class_id)

    # Рисуем боксы и метки
    draw = ImageDraw.Draw(image)
    class_names = ['Bee', 'Wasp']  # Ваши классы

    for box in boxes:
        x1, y1, x2, y2, conf, class_id = box
        label = f"{class_names[class_id]}: {conf:.2f}"
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")

    return image, detected_classes
