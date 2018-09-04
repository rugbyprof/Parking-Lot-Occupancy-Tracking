RESULTS FOLDER
===================

## Purpose
To view the efficacy of the initial lot detection algorithms. This folder only has images. 
The same set of images used in each case. 

The "COLOR ONLY" folder compares the histograms between the defined empty space in the parking lot
and measures the differences.

The "EDGE ONLY" folder compares the amount of white pixels in the black and white image of a space
once the space has been pass through a Python canny-edge detection algorithm. 

The "BOTH" folder displays the images after both of the above algorithms are applied. An occupied space occurs when
EITHER the COLOR or EDGE methods declare a spot to be occupied. 
