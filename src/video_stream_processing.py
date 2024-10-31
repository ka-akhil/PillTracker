import cv2
from src.logger import logging
from asset.config import config


class VideoStreamProcessing:
    @staticmethod
    def initialize_camera(cfg):
        """
        Initializes the camera for video stream processing.

        Args:
            cfg (dict): Configuration dictionary.

        Returns:
            cv2.VideoCapture: The initialized camera object.

        Raises:
            ValueError: If the camera source is invalid.

        """
        # Implementation details...
        camera_source = config.get("camera", {}).get("CAMERA_SOURCE", "")
        cap = cv2.VideoCapture(camera_source)
        if not cap.isOpened():
            logging.error('Invalid video source %s', camera_source, extra={
                'meta': {'label': 'INVALID_VIDEO_SOURCE'},
            })
            raise ValueError("Invalid video source")
        return cap


if __name__ == "__main__":
    VideoStreamProcessing.initialize_camera(config)
