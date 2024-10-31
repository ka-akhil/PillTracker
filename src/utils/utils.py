from typing import List, Tuple
from src.logger import logging
import math


class Rectangle(object):
    @staticmethod
    def get_bounding_box_center(bounding_box: List[int]) -> Tuple[int]:
        """
        Calculates the center point of a bounding box.

        Args:
            boundingBox_1 (List[int]): Representing the coordinates of the bounding boxes in the format [x_min, y_min, x_max, y_max].
            boundingBox_2 (List[int]): representing the coordinates of the bounding boxes in the format [x_min, y_min, x_max, y_max].

        Returns:
            List[int]: Center point coordinates in the format [x_center, y_center].

        Raises:
            ValueError: If the bounding box does not have exactly 4 elements.
        """
        try:
            if bounding_box is None:
                logging.warning(
                    "Bounding box is None. It must be a list or tuple with four elements.")
                raise ValueError(
                    "Bounding box is None. It must be a list or tuple with four elements.")
            elif len(bounding_box) != 4:
                logging.warning(
                    "Invalid number of elements in bounding box. Expected 4 elements.")
                raise ValueError(
                    "Invalid number of elements in bounding box. Expected 4 elements.")
        except ValueError as e:
            return []
        x_center = (bounding_box[0] + bounding_box[2]) / 2
        y_center = (bounding_box[1] + bounding_box[3]) / 2
        return (int(x_center), int(y_center))

    @staticmethod
    def is_overlap(boundingBox_1: List[int], boundingBox_2: List[int], x_percentage: int = 90, y_percentage: int = 90) -> bool:
        """
        Checks if two bounding boxes overlap based on specified overlap percentage thresholds.

        Args:
            boundingBox_1 (List[int]): The coordinates of the first bounding box in the format [x_min, y_min, x_max, y_max].
            boundingBox_2 (List[int]): The coordinates of the second bounding box in the format [x_min, y_min, x_max, y_max].
            x_percentage (int): The minimum overlap percentage required along the x-axis. Defaults to 90.
            y_percentage (int): The minimum overlap percentage required along the y-axis. Defaults to 90.

        Returns:
            bool: True if the bounding boxes overlap based on the specified overlap percentages, False otherwise.

        Raises:
            ValueError: If the bounding boxes do not have exactly 4 elements.
        """

        try:
            if boundingBox_1 is None or boundingBox_2 is None:
                logloggingger.warning(
                    "Bounding box is None. It must be a list or tuple with four elements.")
                raise ValueError(
                    "Bounding box is None. It must be a list or tuple with four elements.")
            elif len(boundingBox_1) != 4 or len(boundingBox_2) != 4:
                logging.warning(
                    "Invalid number of elements in bounding box. Expected 4 elements.")
                raise ValueError(
                    "Invalid number of elements in bounding box. Expected 4 elements.")
        except ValueError as e:
            return False

        x_min1, y_min1, x_max1, y_max1 = boundingBox_1
        x_min2, y_min2, x_max2, y_max2 = boundingBox_2

        x_1 = set(range(math.floor(x_min2), math.ceil(x_max2)))
        x_2 = set(range(math.floor(x_min1), math.ceil(x_max1)))
        x_overlap = x_1.intersection(x_2)
        x_overlap_percentage = max(len(x_overlap) * 100 / (len(x_1) if x_1 else 1),
                                   len(x_overlap) * 100 / (len(x_2) if x_2 else 1))

        y_1 = set(range(math.floor(y_min2), math.ceil(y_max2)))
        y_2 = set(range(math.floor(y_min1), math.ceil(y_max1)))
        y_overlap = y_1.intersection(y_2)
        y_overlap_percentage = max(len(y_overlap) * 100 / (len(y_1) if y_1 else 1),
                                   len(y_overlap) * 100 / (len(y_2) if y_2 else 1))
        # print(x_overlap_percentage, y_overlap_percentage)
        if x_overlap_percentage >= x_percentage and y_overlap_percentage >= y_percentage:
            return True
        return False
