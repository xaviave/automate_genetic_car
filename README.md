# automate_genetic_car

Wrap with a genetic algorithm, the main mission for a dataless "car" is to drive from a point A to a point B.
Power supply is also a big parameter for every car, the consumation will be calculated.
With repetition, random and selection, the car have to "evolve" and adapt itself to any road.

## Car's function

To begin the process, I will let the car know every function then, let the car test and create code with this allowed function

### Functions

- move(x, top_speed)
    x define by the acceleration wanted (could be negative)
- turn(angle, unit="degree")
    could be negative for degree
    unit is default to "degree", could be "radian
- detect(distance, angle, unit="degree", detector="camera")
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
