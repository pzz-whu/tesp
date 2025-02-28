


This example simply verifies that PYPOWER will run a 9-bus case and communicate
over FNCS. To run and plot it:

::

 ./runpp.sh
 python3 plots.py

In addition, traced FNCS messages will be written to pptracer.out

**Directory contents:**

* *clean.sh*; script that removes output and temporary files
* *kill5570.sh*; helper script that stops processes listening on port 5570 (Linux/Mac)
* *NonGLDLoad.txt*; text file of non-responsive loads on transmission buses
* *plots.py*; makes 1 page of plots for a case; eg 'python plots.py'
* *ppcase.json*; PYPOWER system definition
* *pptracer.yaml*; FNCS configuration for the message tracing utility
* *pypower.yaml*; FNCS configuration for PYPOWER
* *README.md*; this file
* *runpp.sh*; script for running the case

Copyright (c) 2017-2022, Battelle Memorial Institute

License: https://github.com/pnnl/tesp/blob/main/LICENSE
