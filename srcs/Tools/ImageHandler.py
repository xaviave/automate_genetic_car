import os
import cv2
import logging
import natsort

import numpy as np

from PIL import Image
from cairosvg import svg2png
from cached_property import cached_property

from Tools.TrackData import TrackData


class ImageHandler:
    """
    Propreties
    """

    @cached_property
    def _light_color_lut(self) -> np.ndarray:
        color0 = np.full((1, 1, 4), (0, 100, 100, 150), np.uint8)
        color1 = np.full((1, 1, 4), (0, 255, 255, 255), np.uint8)
        return self._get_lut(color0, color1, fnull=True)

    @cached_property
    def _sensor_color_lut(self) -> np.ndarray:
        color0 = np.full((1, 1, 4), (0, 0, 100, 255), np.uint8)
        color1 = np.full((1, 1, 4), (0, 0, 255, 255), np.uint8)
        return self._get_lut(color0, color1, fnull=True)

    """
    Private Methods
    """

    @staticmethod
    def _get_lut(
        color0: np.ndarray, color1: np.ndarray, fnull: bool = False
    ) -> np.ndarray:
        """
        create a LUT from color0 to color1,
        first color could be transparent with bnull to erase unwanted background
        """
        lut = np.concatenate((color0, color1), axis=0)
        lut = cv2.resize(lut, (1, 256), interpolation=cv2.INTER_LINEAR)
        if fnull:
            lut[0][0] = [0, 0, 0, 0]
        return lut

    @staticmethod
    def _change_color_map(img: np.ndarray, color_map: np.ndarray) -> np.ndarray:
        """
        apply LUT color map to the img's color range
        """
        dist = img.astype(np.uint8)
        return cv2.LUT(dist, color_map).astype(np.float64)

    @staticmethod
    def _add_text_to_img(
        img: np.ndarray,
        text: str,
        coord: tuple,
        size: float,
        color: tuple = (0, 255, 255, 255),
    ):
        cv2.putText(
            img,
            text,
            coord,
            cv2.FONT_HERSHEY_DUPLEX,
            size,
            color,
            1,
            cv2.LINE_AA,
        )

    def _create_filter(self, track_data: TrackData) -> np.ndarray:
        """
        Add sensor map and light map to create the visual representation
        of the emitter-receptor simulation
        """
        light_map = self._change_color_map(track_data.light_map, self._light_color_lut)
        sensor_map = self._change_color_map(
            track_data.sensor_map, self._sensor_color_lut
        )
        return cv2.addWeighted(sensor_map, 0.5, light_map, 0.5, 0, dtype=cv2.CV_64F)

    """
    Public Methods
    """

    def np_to_img(self, track_map: np.ndarray, track_data: TrackData):
        """
        Create an image with sensor, emitter and track data
        """
        map_filter = self._create_filter(track_data)
        track_map = cv2.addWeighted(
            track_map, 0.5, map_filter, 0.5, 0, dtype=cv2.CV_64F
        )
        track_map[track_data.car_pos[0]][track_data.car_pos[1]] = 255
        self._add_text_to_img(
            track_map,
            track_data.file_name,
            (10, int(0.9 * track_map.shape[1])),
            0.5,
        )
        cv2.imwrite(f"{track_data.file_name}.png", track_map)

    @staticmethod
    def get_img(file_name: str, delete: bool = False) -> np.ndarray:
        img = cv2.imread(f"{file_name}.png", cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        if delete:
            os.remove(f"{file_name}.png")
        return img

    def save_gif(
        self, file_name: str, image_path: str, images: list, delete: bool = False
    ):
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
    def save_png(file_name: str, delete=False):
        with open(f"{file_name}.svg") as image:
            svg_code = image.read()
            svg2png(bytestring=svg_code, write_to=f"{file_name}.png")
        if delete:
            os.remove(f"{file_name}.svg")

    def save_jpg(self):
        pass

    def save_jpeg(self):
        pass
