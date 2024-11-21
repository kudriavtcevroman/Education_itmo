import bentoml
from bentoml.io import Image as BentoImage, JSON
import numpy as np
import onnxruntime as ort
from PIL import Image as PILImage, ImageDraw
import base64
import io
import os

@bentoml.service(name="bee_wasp_detector")
class BeeWaspDetectorService:
    def __init__(self):
        model_path = "/content/yolov8n_SGD.onnx"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Файл модели не найден по пути {model_path}")
        
        # Загрузка модели ONNX
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        # Список имен классов. Расширьте этот список, если модель распознаёт больше классов.
        self.class_names = ['Bee', 'Wasp']
    
    @bentoml.api(input=BentoImage(), output=JSON())
    def predict(self, input_image: PILImage.Image) -> dict:
        # Предобработка изображения
        image = input_image.convert("RGB")
        image_resized = image.resize((640, 640))  # Размер, соответствующий модели YOLOv8
        image_data = np.array(image_resized).astype('float32') / 255.0  # Нормализация
        image_data = image_data.transpose(2, 0, 1)  # Изменение порядка осей: HWC -> CHW
        image_data = np.expand_dims(image_data, axis=0)  # Добавление размерности батча

        # Выполнение инференса
        outputs = self.session.run([self.output_name], {self.input_name: image_data})
        detections = np.squeeze(outputs[0])  # Удаление лишних размерностей

        # Постобработка результатов
        result_image, detected_classes = self.postprocess(detections, image_resized)

        # Конвертация изображения в base64 для передачи через JSON
        buffered = io.BytesIO()
        result_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Получение имен классов из class_ids
        detected_class_names = [self.class_names[class_id] for class_id in detected_classes]

        return {"image_base64": img_str, "detected_classes": detected_class_names}

    def postprocess(self, detections, image):
        """
        Обработка выходных данных модели и рисование bounding boxes.
        """
        # Проверка формы выходных данных
        if detections.ndim == 1:
            detections = detections[np.newaxis, :]  # Добавление размерности, если N=1

        print(f"Количество детекций: {len(detections)}")

        # Порог уверенности
        conf_threshold = 0.1  # Уменьшите порог для проверки

        draw = ImageDraw.Draw(image)

        width, height = image.size

        detected_classes = []  # Список обнаруженных классов

        for detection in detections:
            x1, y1, x2, y2, conf, class_id = detection[:6]

            # Проверяем порог уверенности
            if conf < conf_threshold:
                continue

            # Масштабируем координаты обратно к исходному размеру изображения
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

            # Проверяем валидность class_id
            class_id = int(class_id)
            if class_id < 0 or class_id >= len(self.class_names):
                continue  # Пропускаем, если class_id некорректен

            label = f"{self.class_names[class_id]}: {conf:.2f}"
            print(f"Обнаружен объект: {label} с координатами ({x1}, {y1}), ({x2}, {y2})")

            detected_classes.append(class_id)

            # Рисуем bounding box и метку на изображении
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1 - 10), label, fill="red")

        return image, detected_classes
