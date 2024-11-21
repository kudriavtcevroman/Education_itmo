from __future__ import annotations
import bentoml
import onnxruntime as ort
import numpy as np
from PIL import Image
from bentoml.io import JSON

# BentoML Runnable для выполнения инференса
class ONNXModelRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)  # Можно добавить "gpu", если используется
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        # Загрузка ONNX модели
        self.session = ort.InferenceSession("/content/yolov8n_SGD.onnx")
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    @bentoml.Runnable.method(batchable=False)
    def predict(self, input_sample: dict) -> dict:
        # Предобработка входных данных
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


# Создаём Runner для выполнения инференса
onnx_runner = bentoml.Runner(ONNXModelRunnable)

# BentoML Service для обёртки API
svc = bentoml.Service("onnx_model_service", runners=[onnx_runner])

# API для предсказаний
@svc.api(input=JSON(), output=JSON())
def predict(input_sample: dict) -> dict:
    return onnx_runner.predict.run(input_sample)

