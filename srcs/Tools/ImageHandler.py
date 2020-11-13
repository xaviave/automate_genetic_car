import os
import cv2
import logging
import natsort

import numpy as np

from PIL import Image
from cairosvg import svg2png
from cached_property import cached_property


class ImageHandler:
    @staticmethod
    def _get_lut(color0, color1, fnull=False):
        lut = np.concatenate((color0, color1), axis=0)
        lut = cv2.resize(lut, (1, 256), interpolation=cv2.INTER_LINEAR)
        if fnull:
            lut[0][0] = [0, 0, 0, 0]
        return lut

    @cached_property
    def _light_color_lut(self):
        color0 = np.full((1, 1, 4), (0, 100, 100, 150), np.uint8)
        color1 = np.full((1, 1, 4), (0, 255, 255, 255), np.uint8)
        return self._get_lut(color0, color1, fnull=True)

    @cached_property
    def _sensor_color_lut(self):
        color0 = np.full((1, 1, 4), (0, 0, 100, 255), np.uint8)
        color1 = np.full((1, 1, 4), (0, 0, 255, 255), np.uint8)
        return self._get_lut(color0, color1, fnull=True)

    @staticmethod
    def _change_color_map(img, color_map):
        dist = img.astype(np.uint8)
        return cv2.LUT(dist, color_map).astype(np.float64)

    def np_to_img(self, track_map, track_data):
        light_map = self._change_color_map(track_data.light_map, self._light_color_lut)
        sensor_map = self._change_color_map(
            track_data.sensor_map, self._sensor_color_lut
        )
        map_filter = cv2.addWeighted(
            sensor_map, 0.5, light_map, 0.5, 0, dtype=cv2.CV_64F
        )
        track_map = cv2.addWeighted(
            track_map, 0.5, map_filter, 0.5, 0, dtype=cv2.CV_64F
        )
        track_map[track_data.car_pos[0]][track_data.car_pos[1]] = 255
        cv2.putText(
            track_map,
            track_data.file_name,
            (10, int(0.9 * track_map.shape[1])),
            cv2.FONT_HERSHEY_DUPLEX,
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
