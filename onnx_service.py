from __future__ import annotations
import bentoml
import onnxruntime as ort
import numpy as np
from PIL import Image

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
        Выполнение инференса модели.
        Args:
            input_sample (dict): JSON с путём к изображению.
        Returns:
            dict: Результаты предсказания модели.
        """
        # Предобработка данных
        image_path = input_sample["image_path"]
        image = Image.open(image_path).convert("RGB")

        # Изменение размера до 640x640
        image = image.resize((640, 640))

        # Преобразование изображения в массив
        image_array = np.asarray(image).astype(np.float32)
        image_array = np.transpose(image_array, (2, 0, 1))  # Преобразование в формат CHW
        image_array = np.expand_dims(image_array, axis=0) / 255.0  # Нормализация

        # Выполнение инференса
        predictions = self.session.run([self.output_name], {self.input_name: image_array})

        # Постобработка
        result = predictions[0].tolist()
        return {"predictions": result}
