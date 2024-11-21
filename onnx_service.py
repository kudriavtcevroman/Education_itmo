import bentoml
from bentoml.io import Image
import numpy as np
import onnxruntime as ort
from PIL import Image as PILImage, ImageDraw
import base64
import io

# Определяем сервис
svc = bentoml.Service("bee_wasp_detector")

@svc.on_startup
def load_model(context: bentoml.Context):
    global session, input_name, output_name, class_names
    model_path = "/content/yolov8n_SGD.onnx"
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    # Имена классов
    class_names = ['Bee', 'Wasp']

@svc.api(input=Image(), output=Image())
def predict(input_image: PILImage.Image) -> PILImage.Image:
    # Предобработка изображения
    image = input_image.convert("RGB")
    image_resized = image.resize((256, 256))
    image_data = np.array(image_resized).astype('float32') / 255.0
    image_data = image_data.transpose(2, 0, 1)  # HWC to CHW
    image_data = np.expand_dims(image_data, axis=0)
    
    # Выполнение инференса
    outputs = session.run([output_name], {input_name: image_data})
    
    # Постобработка и рисование результатов
    result_image = postprocess(outputs, image_resized)
    
    return result_image

def postprocess(outputs, image):
    # Обработка выходных данных модели и рисование bounding boxes
    detections = outputs[0]  # Извлекаем предсказания
    detections = np.squeeze(detections)  # Убираем лишние оси
    
    # Транспонируем, если необходимо
    if detections.shape[0] == 6:
        detections = detections.T  # Преобразуем в форму (N, 6)
    
    # Порог уверенности
    conf_threshold = 0.25
    
    draw = ImageDraw.Draw(image)
    
    for detection in detections:
        x1, y1, x2, y2, conf, class_id = detection[:6]
        
        # Проверяем уверенность
        if conf < conf_threshold:
            continue
        
        # Преобразуем координаты к исходному размеру изображения
        width, height = image.size
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height
        
        x1 = int(max(0, x1))
        y1 = int(max(0, y1))
        x2 = int(min(width, x2))
        y2 = int(min(height, y2))
        
        class_id = int(class_id)
        if class_id < 0 or class_id >= len(class_names):
            continue  # Пропускаем, если class_id некорректен
        
        label = f"{class_names[class_id]}: {conf:.2f}"
        
        # Рисуем bounding box и метку
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")
    
    return image
