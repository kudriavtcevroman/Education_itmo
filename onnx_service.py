from __future__ import annotations
import bentoml
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageDraw
import base64
import io

EXAMPLE_INPUT = {"image_path": "/content/Datasets/Bee_or_Wasp_Subset/validation/bees/117423537_2f4372aa4e_m.jpg"}

@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class Model:
    def __init__(self) -> None:
        # Загружаем ONNX модель
        self.session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    @bentoml.api
    def predict(self, input_sample: dict = EXAMPLE_INPUT) -> dict:
        """
        Выполнение инференса модели и возврат изображения с детекцией.
        Args:
            input_sample (dict): JSON с путём к изображению.
        Returns:
            dict: Изображение с детекцией, закодированное в base64.
        """
        # Предобработка данных
        image_path = input_sample["image_path"]
        image = Image.open(image_path).convert("RGB")

        # Изменение размера до 640x640
        image_resized = image.resize((640, 640))

        # Сохраняем копию изображения для рисования bounding box-ов
        draw_image = image_resized.copy()

        # Преобразование изображения в массив
        image_array = np.asarray(image_resized).astype(np.float32)
        image_array = np.transpose(image_array, (2, 0, 1))  # Преобразование в формат CHW
        image_array = np.expand_dims(image_array, axis=0) / 255.0  # Нормализация

        # Выполнение инференса
        predictions = self.session.run([self.output_name], {self.input_name: image_array})

        # Постобработка и рисование bounding box-ов
        result_image = self.postprocess(predictions, draw_image)

        # Конвертация изображения в base64
        buffered = io.BytesIO()
        result_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {"image_base64": img_str}

    def postprocess(self, predictions, image):
        """
        Постобработка выходных данных модели и рисование bounding box-ов.
        Args:
            predictions (list): Сырые выходные данные модели.
            image (PIL Image): Изображение для рисования bounding box-ов.
        Returns:
            PIL Image: Изображение с нарисованными bounding box-ами.
        """
        # Получаем предсказания
        predictions = predictions[0]  # Предполагаем батч размером 1
        # Преобразуем в numpy array
        predictions = np.array(predictions)

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
