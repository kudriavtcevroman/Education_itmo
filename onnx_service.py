from __future__ import annotations
import bentoml
from bentoml.io import Image, JSON
import onnxruntime as ort
import numpy as np
from PIL import Image as PILImage, ImageDraw
import base64
import io

# Используем декоратор @bentoml.service для определения сервиса
@bentoml.service(name="bee_wasp_classifier_service")
class BeeWaspClassifierService:
    def __init__(self):
        # Загружаем модель ONNX
        self.session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    @bentoml.api(input=Image(), output=JSON())
    def predict(self, input_image: PILImage.Image) -> dict:
        # Предобработка изображения
        image = input_image.convert("RGB")
        image_resized = image.resize((640, 640))
        draw_image = image_resized.copy()

        # Преобразование изображения в numpy array
        image_array = np.asarray(image_resized).astype(np.float32)
        image_array = np.transpose(image_array, (2, 0, 1))  # Преобразование в формат CHW
        image_array = np.expand_dims(image_array, axis=0) / 255.0  # Нормализация

        # Выполнение инференса
        predictions = self.session.run([self.output_name], {self.input_name: image_array})

        # Постобработка предсказаний и рисование bounding box-ов
        result_image = self.postprocess(predictions, draw_image)

        # Конвертация изображения в base64
        buffered = io.BytesIO()
        result_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {"image_base64": img_str}

    def postprocess(self, predictions, image):
        # Извлекаем предсказания
        predictions = predictions[0][0]  # Удаляем измерение батча

        if predictions.size == 0:
            return image  # Нет предсказаний

        # Порог уверенности
        conf_threshold = 0.25
        predictions = predictions[predictions[:, 4] >= conf_threshold]

        if predictions.size == 0:
            return image  # Нет предсказаний выше порога

        # Имена классов (обновите в соответствии с вашей моделью)
        class_names = ['bee', 'wasp']

        # Рисование bounding box-ов
        draw = ImageDraw.Draw(image)

        for pred in predictions:
            x1, y1, x2, y2, conf, class_id = pred[:6]
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_id = int(class_id)

            # Проверяем, что class_id в пределах списка class_names
            if class_id >= 0 and class_id < len(class_names):
                label = f"{class_names[class_id]}: {conf:.2f}"
            else:
                label = f"Unknown class {class_id}: {conf:.2f}"

            # Рисуем прямоугольник и метку
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1 - 10), label, fill="red")

        return image
