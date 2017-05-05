Instructions
============
Open Exp1.py

Change the json file loaded as data_file on line 265 as needed
    The json file names are in the format UFPR05_(day).json (where day ranges from 96 to 109)

Change the numImg variable on line 277 to adjust the number of images to run the experiment with
    Use numImg = len(lot_shots) to run on all the images in the json file

Thresholds for the metrics can be adjusted on lines 285 to 289

Run using: python Exp1.py

Output images go to the Output_Images folder in Experiment-1

Red means our metrics determined that the spot was taken
Green means our metrics determined the spot is empty

The Percentage of spots that matched the result from the JSON is printed on the console after each parking lot image is processed.
The overall percentage for the whole experiment is printed last on the console.

