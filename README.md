# RaycastEngine-Py

RaycastEngine-Py is a custom raycast engine programmed in python.
It uses pygame in order to render to a window.
It is simply a raycaster that renders its data, supporting depth and colour.
All walls to be rendered go into an array called "walls", each element being of type "Wall", which takes 4 parameters, a 5th one being optional:
  - X point 1
  - Y point 1
  - X point 2
  - Y point 2
  - (R, G, B) color value *optional*

# Dependencies

In order to run from source, you must have:
 - A python interpreter
 - Python math library
 - Python pygame library

# How to run

Executable binary files are available on the releases page if you do not want to or cannot run it from source.
