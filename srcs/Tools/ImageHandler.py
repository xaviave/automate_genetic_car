import os
import cv2
import logging
import natsort

import numpy as np

from PIL import Image
from cairosvg import svg2png


class ImageHandler:
    _light_color: np.array = np.array([0, 50, 255, 255])
    _sensor_color: np.array = np.array([255, 50, 0, 255])

    @staticmethod
    def _get_filter(bin_map, color):
        pixel_filter = np.repeat(bin_map[:, :, np.newaxis], 4, axis=2)
        pixel_light_mask = (pixel_filter > [0, 0, 0, 0]).all(axis=2)
        pixel_filter[pixel_light_mask] = color
        return pixel_filter

    def np_to_img(self, track_map, track_data):
        map_filter = cv2.add(
            self._get_filter(track_data.light_map, self._light_color),
            self._get_filter(track_data.sensor_map, self._sensor_color),
        )
        track_map = cv2.addWeighted(
            track_map, 0.7, map_filter, 0.3, 0, dtype=cv2.CV_64F
        )
        track_map[track_data.car_pos[0]][track_data.car_pos[1]] = 255
        cv2.putText(
            track_map,
            track_data.file_name,
            (10, int(0.9 * track_map.shape[1])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.imwrite(f"{track_data.file_name}.png", track_map)

    @staticmethod
    def get_img(file_name, delete=False):
        img = cv2.imread(f"{file_name}.png", cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
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
            duration=5,
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
