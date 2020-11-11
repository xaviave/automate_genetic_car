import os
import cv2
import logging
import natsort

import numpy as np

from PIL import Image
from cairosvg import svg2png


class ImageHandler:
    _light_color: np.array = np.array([0.9, 1, 0.2])
    _sensor_color: np.array = np.array([0.8, 0, 0.1])

    @staticmethod
    def _get_filter(bin_map, color):
        pixel_filter = np.repeat(bin_map[:, :, np.newaxis], 3, axis=2)
        pixel_mask = (pixel_filter > [0, 0, 0]).all(axis=2)
        pixel_filter[pixel_mask] = color
        return pixel_filter

    def np_to_img(self, file_name, track_map, light_map, sensor_map, car_pos):
        map_filter = cv2.add(
            self._get_filter(light_map, self._light_color),
            self._get_filter(sensor_map, self._sensor_color),
        )
        track_map = cv2.addWeighted(
            track_map, 0.5, map_filter, 0.5, 0, dtype=cv2.CV_64F
        )
        track_map[car_pos[0]][car_pos[1]] = 1
        cv2.imwrite(f"{file_name}.png", track_map)

    @staticmethod
    def get_img(file_name, delete=False):
        img = cv2.imread(f"{file_name}.png")
        if delete:
            os.remove(f"{file_name}.png")
        return img

    def save_gif(self, file_name, image_path, images, delete=False):
        img, *imgs = [
            Image.open(os.path.join(image_path, f)) for f in natsort.natsorted(images)
        ]
        img.save(
            fp=file_name,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=200,
            loop=0,
        )
        logging.info(f"GIF save at {file_name} successfully")
        if delete:
            for i in images:
                os.remove(os.path.join(image_path, i))
            os.rmdir(image_path)


    @staticmethod
    def save_png(file_name, delete=False):
        with open(f"{file_name}.svg") as image:
            svg_code = image.read()
            svg2png(bytestring=svg_code, write_to=f"{file_name}.png")
        if delete:
            os.remove(f"{file_name}.svg")

    def save_jpg(self):
        pass

    def save_jpeg(self):
        pass
