# Turtle Simulation using ROS2

## Summary
This project implements turtle simulation tasks using ROS2 and Python.

## Features
- Shape Drawing (Square, Triangle)
- Navigation to given coordinates
- GUI controls (Reset, Clear)
- Follow the Girl (two turtles with tracking)

## Requirements
- ROS2 Jazzy
- Python 3

## How to Run

1. Start turtlesim:
   ros2 run turtlesim turtlesim_node

2. Run Shape:
   python3 shape/draw_square.py
   python3 shape/draw_triangle.py

3. Run Navigation:
   python3 navigation/navigate.py

4. Run GUI:
   python3 gui/gui_control.py

5. Run Follow:
   python3 follow/follow_turtle.py
