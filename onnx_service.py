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
@svc.on_startup
def load_model(context: bentoml.Context):
    global session, input_name, output_name
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
    image_array = np.asarray(image_resized).astype(np.float32) / 255.0
    image_array = np.transpose(image_array, (2, 0, 1))
    image_array = np.expand_dims(image_array, axis=0)

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
    # Отладочный вывод
    print(f"Тип predictions: {type(predictions)}")
    print(f"Длина predictions: {len(predictions)}")
    print(f"Форма predictions[0]: {predictions[0].shape}")
    print(f"Содержимое predictions[0]:\n{predictions[0]}")
    
    # Извлекаем предсказания
    predictions = predictions[0]  # Удаляем внешний список

    # Если предсказаний нет, возвращаем исходное изображение и пустой список
    if predictions.size == 0:
        return image, []

    # Преобразуем предсказания в нужную форму
    predictions = np.squeeze(predictions)

    # Порог уверенности
    conf_threshold = 0.25

    # Имена классов
    class_names = ['Bee', 'Wasp']

    # Получаем размеры изображения
    width, height = image.size

    # Списки для обнаруженных объектов
    boxes = []
    detected_classes = []

    # Пробегаем по каждому предсказанию
    for pred in predictions:
        # Извлекаем координаты и другие параметры
        x1, y1, x2, y2, obj_conf, class_conf = pred[:6]
        class_scores = pred[5:]  # Вероятности классов

        # Вычисляем общую уверенность
        conf = obj_conf * class_conf

        if conf < conf_threshold:
            continue  # Пропускаем предсказания с низкой уверенностью

        # Определяем идентификатор класса
        class_id = int(np.argmax(class_scores))

        # Масштабируем координаты до размеров изображения
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height

        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Добавляем информацию об объекте
        boxes.append([x1, y1, x2, y2, conf, class_id])
        detected_classes.append(class_names[class_id])

    # Рисуем bounding box-ы и метки
    draw = ImageDraw.Draw(image)
    for box in boxes:
        x1, y1, x2, y2, conf, class_id = box
        label = f"{class_names[class_id]}: {conf:.2f}"
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")

    return image, detected_classes
