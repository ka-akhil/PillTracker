
import cv2
import os
import time
from asset.config import config
from src.logger import logging
from src.inference import YoloInference
from src.utils.utils import Rectangle
from src.video_stream_processing import VideoStreamProcessing


class PillTracker:
    """
    A class that tracks pills in a video frame.

    Attributes:
        frame: The current frame of the video.
        frame_height: The height of the frame.
        frame_width: The width of the frame.
        detector: The object used for pill detection.
        frame_detection_details: The details of pill detection in the frame.
        area_of_interest: The coordinates of the area of interest for pill counting.

    Methods:
        __init__(self, initial_frame, detector): Initializes a PillTracker object.
        process_frame(self): Processes the current frame and returns the pill count and the frame.
        visualize_frame(self, pill_count): Visualizes the frame with the pill count.
        set_area_of_interest(self, square_size): Sets the area of interest for pill counting.
        count_pills(self): Counts the number of pills in the frame.
    """

    def __init__(self, initial_frame, detector):
        self.frame = initial_frame  # current frame of video
        self.frame_height = initial_frame.shape[0]
        self.frame_width = initial_frame.shape[1]
        self.detector = detector
        self.frame_detection_details = None
        self.area_of_interest = self.set_area_of_interest()

    def process_frame(self):
        """
        Process a frame by performing pill detection and counting.

        Returns:
            tuple: A tuple containing the pill count and the processed frame.
                The pill count is a dictionary with the 'total_count' key representing
                the total number of pills detected. The processed frame is the input frame
                after visualization.

        """
        try:
            self.frame_detection_details = self.detector.predict(self.frame)
            pill_count = self.count_pills()
            self.visualize_frame(pill_count.get('total_count', 0))
            return pill_count, self.frame
        except Exception as e:
            logging.error(e)
            return {'total_count': 0}, self.frame

    def visualize_frame(self, pill_count):
        """
        Visualizes the frame with the pill count.

        Args:
            pill_count (int): The number of pills detected.

        Returns:
            numpy.ndarray: The processed frame with the pill count.

        """
        try:
            text_at_top = "Pill Count: {}".format(pill_count)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.frame, text_at_top, (50, 50),
                        font, 1, (0, 0, 0), 2, cv2.LINE_4)
            return self.frame
        except Exception as e:
            logging.error(e)
            return self.frame

    def set_area_of_interest(self, square_size=500):
        """
        Sets the area of interest for pill counting.

        Args:
            square_size (int): The size of the square area of interest.

        Returns:
            list: The coordinates of the area of interest in the format [x1, y1, x2, y2].

        """
        try:
            center_x, center_y = self.frame_width // 2, self.frame_height // 2
            square_half = square_size // 2
            # Calculate square coordinates
            x, y = center_x - square_half, center_y - square_half

            color = (0, 255, 0)  # Green
            thickness = 2
            start_point = (x, y)
            end_point = (x + square_size, y + square_size)
            cv2.rectangle(self.frame, start_point, end_point, color, thickness)
            return [start_point[0], start_point[1], end_point[0], end_point[1]]
        except Exception as e:
            logging.error(e)
            return [0, 0, 0, 0]

    def count_pills(self):
        """
        Counts the number of pills in the frame.

        Returns:
            dict: A dictionary containing the total count of pills.

        """
        try:
            pill_count = 0
            for pill_bbox in self.frame_detection_details['bbox']:
                if Rectangle.is_overlap(pill_bbox, self.area_of_interest, y_percentage=10, x_percentage=10):
                    pill_count += 1
                    center = Rectangle.get_bounding_box_center(pill_bbox)
                    self.frame = cv2.circle(
                        self.frame, center, 4, (0, 255, 255), -1)
            return {'total_count': pill_count}
        except Exception as e:
            logging.error(e)
            return {'total_count': 0}


def run():
    # Initialize the model
    detector = YoloInference(config.get("model", {}).get("MODEL_PATH", ""))
    vid_reader = VideoStreamProcessing.initialize_camera(config)
    retval, frame = vid_reader.read()

    if config.get("save_video", {}).get("SAVE_VIDEO", ""):
        if not os.path.exists(config.get("save_video", {}).get("SAVE_VIDEO_PATH", "")):
            logging.error(
                "Please provide a path to save the video in the config file.")
            return

    result = cv2.VideoWriter(config.get("save_video", {}).get("SAVE_VIDEO_PATH", "") + "output.avi",
                             cv2.VideoWriter_fourcc(
                                 *config.get("save_video", {}).get("SAVE_VIDEO_CODEC", "")),
                             config.get("save_video", {}).get("SAVE_VIDEO_FPS", ""), (config.get("save_video", {}).get("SAVE_VIDEO_WIDTH", ""), config.get("save_video", {}).get("SAVE_VIDEO_HEIGHT", "")))
    while retval:
        pill_tracker = PillTracker(frame, detector)

        try:
            count, processed_frame = pill_tracker.process_frame()
            print(count)
            result.write(processed_frame)
            cv2.imshow('Frame', processed_frame)
            cv2.waitKey(1)
            retval, frame = vid_reader.read()

        except Exception as e:
            logging.error(e)
    vid_reader.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
