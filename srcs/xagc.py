import os

from CarUtils.Car import Car
from CarUtils.Motor import Motor
from CarUtils.Sensor import Sensor
from CarUtils.Headlight import Headlight
from Tools.ImageHandler import ImageHandler
from TrackUtils.TrackGenerator import TrackGenerator

"""
    Launcher for the Automate Genetic algorithm Car
    
    fitness is really simple: percentage of the car distance to the last point
    also the fitness will stop at the percentile if the car touch the grass
    
    multi parameter are used here:
        - motors to move with two parameters
        - headlight to let the sensor "see" with four parameters
        - sensor to detect the track environment with four parameters
        - power_utils that allow the power consumption that affect everything
          for better precision of the model with two parameters 

    v0 - Only use motors and sensors with only angle with
         infite vision range and top speed. No power nor light.
         Optimisation will apply with 2 big angle sensors and a motor

"""


def main():
    track = TrackGenerator()
    track_map = ImageHandler().get_img(track.file_name, delete=True)
    m = Motor(100, 100)
    s = Sensor((0, 0), 10, 90, 180)
    h = Headlight((0, 0), 10, 90, 180)
    c = Car((0, 0), sensors=[s, s], headlights=[h], motors=[m], power_utils=[])
    c.launch(track_map, gif=True)


if "__main__" == __name__:
    main()
