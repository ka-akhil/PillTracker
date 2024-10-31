from ultralytics import YOLO
from src.logger import logging


class YoloInference():
    def __init__(self, weight_path: str) -> None:
        logging.info(f"Initializing model with weights at {weight_path}")
        self.model = YOLO(weight_path)
        logging.info(f"Model running on {self.model.device}")

    def predict(self, img_path: str, save_path: str = "\out", save_image: bool = False, confidence: float = 0.8, iou: float = 0.5, img_size: tuple = (416, 416), class_id: int = 0, save_text: bool = False) -> tuple:
        """
        Predicts the bounding boxes, class IDs, and confidence scores for objects in an image.

        Args:
            img_path (str): The path to the input image.
            save_path (str, optional): The path to save the output image. Defaults to "\out".
            save_image (bool, optional): Whether to save the output image. Defaults to False.
            confidence (float, optional): The confidence threshold for object detection. Defaults to 0.8.
            iou (float, optional): The intersection over union threshold for non-maximum suppression. Defaults to 0.5.
            img_size (tuple, optional): The size of the input image. Defaults to (416, 416).
            class_id (int, optional): The class ID to filter the predictions. Defaults to 0.
            save_text (bool, optional): Whether to save the output text file. Defaults to False.

        Returns:
            tuple: A tuple containing the bounding boxes, class IDs, and confidence scores for the detected objects.
        """
        try:
            prediction = self.model.predict(
                img_path, save=False, conf=confidence, iou=iou, imgsz=img_size, classes=class_id, save_txt=save_text, line_width=1, show_labels=True)

            final_result = {'bbox': prediction[0].boxes.xyxy.detach().cpu().numpy().tolist(),
                            'cls_id': prediction[0].boxes.cls.detach().cpu().numpy().tolist(),
                            'conf': prediction[0].boxes.conf.detach().cpu().numpy().tolist()}

            return final_result
        except Exception as e:
            logging.error(f"An error occurred during prediction: {str(e)}")
            return None
