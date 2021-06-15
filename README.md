# AtwoodSolver
The repository consists of an end-to-end pipeline for interpreting and solving Atwood Systems.

The current version has the following Assumptions:
1. The image processing performs well mostly on a single type of pulley system images as shown below on other images, it may or may not perform well.
2. Single pulley System is assumed, so pulley systems involving multiple pulley is yet to be done(image processing part detects the objects, pulleys and wedges, but no relation can be established among them).
3. String is not detected, single pulley system assumes the use of single string.
4. Solver is designed assuming only the force components along the direction of string, no other equation like string constraints, normal equations, forces on non stationary pulley, etc is considere yet.

![alt text](https://github.com/Piyush-Kumar-Behera/AtwoodSolver/blob/main/images/Pulley_Ex3.png?raw=True)


## Installation and Testing:
After cloning the repo,

```shell
python -m pip install -r requirements.txt
```
To run the repo with default image:
```shell
python main.py
```
or with a particular image:
```shell
python main.py -i image_loc
