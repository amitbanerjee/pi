# File List

## README.md - This file. It describes The contents of the package and how to run the program
## HighLevelDesign.txt - This if the high level design doc
## newPackage.py - This implements the shared data structure of the packages with a mutex on all read/write operation 
## piServer.py - This implements the tcp sockes and it imports newPackage for internal use.

# How to run (It needs Pythin 2.7). Use the following command to run. It attaches itself to the terminal prints the log on the terminal.

## "python piServer.py"
## To detach it from terminal and redirect log to a log file use "nohup python piServer.py > log file &"

# Note: It is tested successfully with the supplied testing suits "do-package-tree_linux" and it passed all the tests in 9441ms
