# Track Generator

Generate maps that the Automate Genetic Car will use to train on.


## 2D track

Launch with: `python3 xagc.py track`

Generate the track SVG in data/tracks

### Prerequisites

Install cairo `sudo apt-get install libcairo2`

Then: `pip3 install requirements/requirements.txt`

### Colors

The colors allow the car's sensor to detect the environment.

    black: road
    green: grass
    
version 0: Only detect the road and the grass, no obstacles or different road's types

### Algorithm

Following parameters, a line will start from a random point in the left side of the SVG connect to the right side.
Difficulty parameters will add points in the SVG to add curves on the line.

    Difficulty: 1-10, add points in a range around the start point.
    Curves: 1-3, define the hardness of the curves.
    Size: define the Width and the Height. 
 
 
