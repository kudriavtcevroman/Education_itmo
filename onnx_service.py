from __future__ import annotations
import bentoml
import onnxruntime as ort
import numpy as np
from PIL import Image
from bentoml.io import JSON

# Создаём BentoML сервис с использованием декоратора
@bentoml.service()
class ONNXModelService:
    def __init__(self):
        # Загрузка ONNX модели
        self.session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    @bentoml.api(input=JSON(), output=JSON())
    async def predict(self, input_sample: dict) -> dict:
        """
        Выполнение инференса модели.
        Args:
            input_sample (dict): JSON с путём к изображению.
        Returns:
            dict: Результаты предсказания модели.
        """
        # Предобработка изображения
        image_path = input_sample["image_path"]
        image = Image.open(image_path).convert("RGB")
        image_array = np.asarray(image).astype(np.float32)
        image_array = np.transpose(image_array, (2, 0, 1))  # Преобразование в CHW
        image_array = np.expand_dims(image_array, axis=0) / 255.0  # Нормализация

        # Выполнение инференса
        predictions = self.session.run([self.output_name], {self.input_name: image_array})

        # Постобработка результатов
        result = predictions[0].tolist()
        return {"predictions": result}
