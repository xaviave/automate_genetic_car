import numpy as np

from CarUtils.GeneticCar import GeneticCar


def main():
    f = GeneticCar(
        10, mutation=4, timer=30, avoid=np.array([0, 128, 0, 255], dtype=np.uint8)
    )
    f.launch()


if "__main__" == __name__:
    main()
