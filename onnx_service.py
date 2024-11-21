import bentoml
from bentoml.io import Image as BentoImage, JSON
import numpy as np
import onnxruntime as ort
from PIL import Image as PILImage, ImageDraw
import base64
import io
import os

# Определяем сервис
svc = bentoml.Service("bee_wasp_detector")

# Загрузка модели при инициализации модуля
model_path = "/content/yolov8n_SGD.onnx"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Файл модели не найден по пути {model_path}")

session = ort.InferenceSession(model_path)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
class_names = ['Bee', 'Wasp']  # Расширьте этот список, если модель распознаёт больше классов

@svc.api(input=BentoImage(), output=JSON())
def predict(input_image: PILImage.Image) -> dict:
    # Предобработка изображения
    image = input_image.convert("RGB")
    image_resized = image.resize((256, 256))  # Убедитесь, что размер соответствует модели
    image_data = np.array(image_resized).astype('float32') / 255.0  # Нормализация
    image_data = image_data.transpose(2, 0, 1)  # HWC to CHW
    image_data = np.expand_dims(image_data, axis=0)  # Добавляем размерность батча

    # Выполнение инференса
    outputs = session.run([output_name], {input_name: image_data})  # Исправлено на image_data

    # Постобработка и рисование результатов
    result_image, detected_classes = postprocess(outputs, image_resized)

    # Конвертация изображения в base64
    buffered = io.BytesIO()
    result_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": img_str, "detected_classes": detected_classes}

def postprocess(outputs, image):
    # Обработка выходных данных модели и рисование bounding boxes
    detections = outputs[0]  # Извлекаем предсказания
    detections = np.squeeze(detections)  # Убираем лишние оси

    # Транспонируем, если необходимо
    if detections.shape[0] == 6:
        detections = detections.T  # Преобразуем в форму (N, 6)

    print(f"Количество детекций: {len(detections)}")

    # Порог уверенности
    conf_threshold = 0.1  # Уменьшите порог для проверки

    draw = ImageDraw.Draw(image)

    width, height = image.size

    detected_classes = []  # Список обнаруженных классов

    for detection in detections:
        x1, y1, x2, y2, conf, class_id = detection[:6]

        # Проверяем уверенность
        if conf < conf_threshold:
            continue

        # Преобразуем координаты к исходному размеру изображения
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height

        # Преобразуем координаты в целые числа
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Убедимся, что x1 <= x2 и y1 <= y2
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Ограничиваем координаты размерами изображения
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        class_id = int(class_id)
        if class_id < 0 or class_id >= len(class_names):
            continue  # Пропускаем, если class_id некорректен

        label = f"{class_names[class_id]}: {conf:.2f}"
        print(f"Обнаружен объект: {label} с координатами ({x1}, {y1}), ({x2}, {y2})")

        detected_classes.append(class_id)

        # Рисуем bounding box и метку на изображении
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")

    return image, detected_classes
