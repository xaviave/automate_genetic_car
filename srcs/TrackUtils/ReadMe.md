# Track Generator

Generate maps that the Automate Genetic Car will use to train on.


## 2D track

Launch with: `python3 srcs/xtrack.py`

Generate the track SVG in data/tracks
Options allows you to convert SVG into image's types of your choices.
See all options in usage with: `python3 srcs/xtrack.py -h`  

### Colors

The colors allow the car's sensor to detect the environment.

    black: road
    green: grass
    
version 0: Only create the road and the grass, no obstacles or different road's types no curves too

### Algorithm

Following parameters, a line will start from a random point in the left side of the SVG connect to the right side.
Difficulty parameters will add points and curves indices that will complexify the line drawing.

    Difficulty: 1-3
 
  
## Prerequisites

Install cairo `sudo apt install libcairo2`

Then: `pip3 install requirements/requirements.txt`
