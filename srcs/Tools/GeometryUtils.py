import cv2
import numpy as np


class GeometryUtils:
    @staticmethod
    def _rotate_around_point(vec, angle) -> np.array:
        rotate = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        return np.dot(rotate, vec)

    def _get_triangle_mask(self, array, ref_vec, ref_point, angle0, angle1):
        vec1 = np.add(self._rotate_around_point(ref_vec, angle0), ref_point)
        vec2 = np.add(self._rotate_around_point(ref_vec, angle1), ref_point)
        pts = np.array([[ref_point, vec1, vec2]], dtype=np.int32)
        cv2.fillPoly(array, pts, (1, 0, 0, 255))
        return 1 * np.all(array == np.array([1, 0, 0, 255]), axis=2)

    @staticmethod
    def _bin_to_img(bin_map):
        """
        create a filter img from a bin map
        """
        bin_map = bin_map.astype(np.uint8)
        img = np.repeat(bin_map[:, :, np.newaxis], 4, axis=2)
        img_mask = (img > [0, 0, 0, 0]).all(axis=2)
        img[img_mask] = 255
        return img

    def _intensity_map(self, img, bin_map=False):
        """
        :param img: type must be np.uint8
        """
        if bin_map:
            img = self._bin_to_img(1 * img)
        dist = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dist = cv2.distanceTransform(dist, cv2.DIST_C, 3)
        cv2.normalize(dist, dist, 0, 255, cv2.NORM_MINMAX)
        return np.repeat(dist[:, :, np.newaxis], 4, axis=2)
