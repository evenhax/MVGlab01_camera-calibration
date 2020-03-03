# CameraCaliPython
## Introduction
The demo for single camera calibration by a 3d-rig picture.
And it is compiled by Pycharm, use python3 and a library named numpy.
There are several steps in this demo:
1. Choose a picture of 3D-rig online, as shown in *Jietu20200301-091513.jpg*
Though we do not have a real rig, but this would not change the core method of camera calibration because 
it's okay to assume that the length and width of each small square is the unit length.
2. Mark some cross points by Labelme (or any other app with similar function) and record the pixel coordinate of them with the correspondings
in world coordinate system. In this demo, the three intersections of planes are chosen as x,y and z axis of world coordinate system, which 
follow right-handed system.  (as shown in *Jietu20200301-091513.jpg*)
In this demo, 12 points are chosen. Generally speaking, though 6 points are enough theoretically, more points are good for the precesion of camera matrix estimation. 
3. Use the chosen points to work out M, K, R,t by methods on class.
4. To verify the calibration results, we:
