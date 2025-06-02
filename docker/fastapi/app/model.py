from ultralytics import YOLO
import supervision as sv

def model_init():
    model = YOLO("yolo11n.pt")
    #model = YOLO("https://hub.ultralytics.com/models/ahJ26xzlb1ncruCZlpTv")
    return model

def model_detect(model,image):
    results = model(image)
    return parse_detections(str(results))

def parse_detections(result):
    output = sv.Detections.from_ultralytics(result)
    return output