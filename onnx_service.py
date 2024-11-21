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
    # Извлекаем предсказания
    predictions = predictions[0][0]  # Удаляем измерение батча

    if predictions.size == 0:
        return image, []  # Нет предсказаний

    # Порог уверенности
    conf_threshold = 0.25
    predictions = predictions[predictions[:, 4] >= conf_threshold]

    if predictions.size == 0:
        return image, []  # Нет предсказаний выше порога

    # Имена классов (обновите в соответствии с вашей моделью)
    class_names = ['bee', 'wasp']

    # Получаем размеры изображения
    width, height = image.size

    # Рисование bounding box-ов
    draw = ImageDraw.Draw(image)

    detected_classes = []

    for pred in predictions:
        x1, y1, x2, y2, conf, class_id = pred[:6]

        # Если координаты нормализованы, масштабируем их
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height

        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        class_id = int(class_id)

        # Проверяем, что class_id в пределах списка class_names
        if 0 <= class_id < len(class_names):
            label = f"{class_names[class_id]}: {conf:.2f}"
            detected_classes.append(class_names[class_id])
        else:
            label = f"Unknown class {class_id}: {conf:.2f}"
            detected_classes.append(f"Unknown class {class_id}")

        # Убедимся, что x1 <= x2 и y1 <= y2
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Ограничиваем координаты размером изображения
        x1 = max(0, min(x1, width - 1))
        x2 = max(0, min(x2, width - 1))
        y1 = max(0, min(y1, height - 1))
        y2 = max(0, min(y2, height - 1))

        # Рисуем прямоугольник и метку
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")

    return image, detected_classes
