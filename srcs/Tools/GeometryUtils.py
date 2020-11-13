import cv2
import numpy as np


class GeometryUtils:
    @staticmethod
    def _rotate_around_point(vec: np.array, angle: float) -> np.array:
        rotate = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        return np.dot(rotate, vec)

    def _get_triangle_mask(
        self,
        array: np.array,
        ref_vec: np.array,
        ref_point: tuple,
        angle0: float,
        angle1: float,
    ) -> np.ndarray:
        vec1 = np.add(self._rotate_around_point(ref_vec, angle0), ref_point)
        vec2 = np.add(self._rotate_around_point(ref_vec, angle1), ref_point)
        pts = np.array([[ref_point, vec1, vec2]], dtype=np.int32)
        cv2.fillPoly(array, pts, (1, 0, 0, 255))
        return 1 * np.all(array == np.array([1, 0, 0, 255]), axis=2)

    @staticmethod
    def _bin_to_img(bin_map: np.ndarray) -> np.ndarray:
        """
        create a filter img from a bin map
        """
        bin_map = bin_map.astype(np.uint8)
        img = np.repeat(bin_map[:, :, np.newaxis], 4, axis=2)
        img_mask = (img > [0, 0, 0, 0]).all(axis=2)
        img[img_mask] = 255
        return img

    def _intensity_map(self, img: np.ndarray, bin_map: bool = False) -> np.ndarray:
        """
        Ratio the intensity of the light from the center to the corner of the polygon

        TO-DO: Ratio the intensity of the light value with diff point-car coord value
        :param img: type must be np.uint8
        """
        if bin_map:
            img = self._bin_to_img(1 * img)
        dist = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dist = cv2.distanceTransform(dist, cv2.DIST_C, 3)
        cv2.normalize(dist, dist, 0, 255, cv2.NORM_MINMAX)
        return np.repeat(dist[:, :, np.newaxis], 4, axis=2)
