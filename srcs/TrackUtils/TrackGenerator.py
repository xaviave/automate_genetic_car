import os
import sys
import random
import logging
import datetime
import svgwrite

from svgwrite import cm, mm
from Tools.ArgParser import ArgParser
from Tools.ImageHandler import ImageHandler
from TrackUtils.TrackComplexity import TrackComplexity
from TrackUtils.TrackEnvironment import TrackEnvironment


class TrackGenerator(ArgParser):
    file_name: str
    points: list = []
    default_path = os.path.join("data", "tracks")
    default_environment = TrackEnvironment.list()

    """
    Overriding methods
    """

    def _add_parser_args(self, parser):
        super()._add_parser_args(parser)
        parser.add_argument(
            "-d",
            "--difficulty",
            type=int,
            default=TrackComplexity.D1,
            dest="complexity",
            help="Choose the complexity of the track",
        )
        # parser.add_argument(
        #     "-e",
        #     "--environment",
        #     action="store_append",
        #     default=TrackEnvironment.list(),
        #     help="Choose the Environment of the track",
        # )
        parser.add_argument(
            "-ww",
            "--width",
            type=int,
            default=500,
            help="Define the Width of the track, min 50",
        )
        parser.add_argument(
            "-hh",
            "--height",
            type=int,
            default=500,
            help="Define the Height of the track, min 50",
        )
        parser.add_argument(
            "-p",
            "--path",
            type=str,
            default=self.default_path,
            help="Path directory for track's file",
        )

    def _add_exclusive_args(self, parser):
        super()._add_exclusive_args(parser)
        sp = parser.add_mutually_exclusive_group(required=False)
        sp.add_argument(
            "--png",
            action="store_const",
            const=ImageHandler.save_png,
            dest="image_type_func",
            help="Default image type",
        )
        sp.add_argument(
            "--jpg",
            action="store_const",
            const=ImageHandler.save_jpg,
            dest="image_type_func",
        )
        sp.add_argument(
            "--jpeg",
            action="store_const",
            const=ImageHandler.save_jpeg,
            dest="image_type_func",
        )

    def _get_options(self):
        super()._get_options()
        if not os.path.exists(self.args.path):
            os.makedirs(self.args.path)
            logging.info(
                f"Directory does not exist. '{self.args.path}' is now created."
            )
        if self.args.height < 50 or self.args.width < 50:
            self._exit(message="Height and Width must be greater than 50")
        if self.args.image_type_func is None:
            logging.info("Use default")
            self.args.image_type_func = ImageHandler.save_png
        self.args.complexity = TrackComplexity.list()[self.args.complexity - 1]

    """
        Private methods
    """

    @staticmethod
    def _exit(exception=None, message="Error", flag=-1):
        if exception:
            logging.error(f"{exception}")
        logging.error(f"{message}")
        sys.exit(flag)

    @staticmethod
    def _generate_point(last_point, x, y, range_x=0, range_y=0) -> tuple:
        """
        :param range_x: range between the x given
        :param range_y: range between the y given
        """
        min_x = x - range_x if x - range_x > last_point[0] else last_point[0] + range_x
        min_y = y - range_y if y - range_y > last_point[1] else last_point[1] + range_y
        px = abs(random.randint(abs(min_x), x + range_x))
        py = abs(random.randint(abs(min_y), y + range_y))
        return px, py

    def _generate_map(self, width, height):
        dwg = svgwrite.Drawing(
            filename=f"{self.file_name}.svg",
            size=(width, height),
        )
        rect = dwg.add(dwg.g(id="background"))
        rect.add(dwg.rect((0, 0), (width, height), fill="green"))
        logging.info(self.points)
        line_width = self.get_args("complexity").value.width
        polyline = dwg.add(dwg.g(id="polyline"))
        polyline.add(
            dwg.polyline(
                self.points,
                stroke_width=line_width,
                stroke="black",
                fill="black",
                fill_opacity=0.0,
            )
        )
        dwg.save()

    def _generate_road(self, width, height):
        x = 0
        y = 0
        complexity = self.get_args("complexity").value
        for i in range(complexity.points):
            last_point = (x, y)
            if i == complexity.points - 1:
                x = width
                y = height
            elif i > 0:
                x = int(width / (complexity.points - i))
                y = int(height / (complexity.points - i))
            self.points.append(
                self._generate_point(
                    last_point,
                    x=x,
                    y=y,
                    range_x=i * complexity.curves,
                    range_y=i * complexity.curves,
                )
            )

    """
        Public methods
    """

    def __init__(self):
        super().__init__()
        self.file_name = os.path.join(
            self.get_args("path"),
            f"Track_{self.get_args('complexity').value}_{datetime.datetime.now()}",
        )
        logging.info(self.args)
        self.generate_track()

    def generate_track(self):
        width = self.get_args("width")
        height = self.get_args("height")
        self._generate_road(width, height)
        self.points.append((510, 510))
        self._generate_map(width, height)
        self.get_args("image_type_func")(self.file_name, delete=True)
