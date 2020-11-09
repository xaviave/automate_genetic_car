# automate_genetic_car

Wrap with a genetic algorithm, the main mission for a dataless "car" is to drive from a point A to a point B.
Power supply is also a big parameter for every car, the consumation will be calculated.
With repetition, random and selection, the car have to "evolve" and adapt itself to any road.

## Track generator

To train these little evolutive car we need to create random playground. Cars like road but not grass so I star with this.

`xtrack.py` is a minimal track creator with color with signification obviously and a pattern for road that cross a SVG file.
Options are used to create complexity because our cars will be better and better.
Their is a track generator `ReadMe` in *srcs/TrackUtils/*

## Car's function

To begin the process, I will let the car know every function then, let the car test and create code with this allowed function

### Functions

- move(x, top_speed)
    x define by the acceleration wanted (could be negative)
- turn(angle, unit="degree")
    could be negative for degree
    unit is default to "degree", could be "radian
- detect(intensity, angle, unit="degree", sensor="camera")
    distance is set the max distance detection
    angle could be negative for degree,
    unit is default to "degree", could be "radian)
    detector is the detector type (just camera for now, it's default)
- headlight(intensity, color)
    intensity is the power supplies to the headlight
    color is define by the object color. Depending of the type color, it will work for just a type of detector.

## Power supply

The main problematic is to define the power consumption of every component or function here to simulate a electric car.
The weight and aerodynamic of the car have to count in the calculus.
The battery stockage and power supply need to be given as parameter to allow different simulation type.
Stop the car when there's no more power allow a new good parameter to test and create car.

## Links

https://docs.google.com/document/d/1ZSVyajzm0fQe7fPy5RVXt3ifOAFmoWJv5zQjS9kkFco/edit

## Prerequisities

Launch those command in your terminal

    sudo apt update
    sudo apt upgrade
    sudo apt install python3 python3-pip libcairo2 
    pip3 install -r requirements/requirements.py
    pre-commit
