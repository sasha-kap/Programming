Instructions for running the code on Mac:

Note: Code is written for Python version 2.7.

Code can be run directly in Python or from a Jupyter notebook (if installed).  

Running code directly on Mac:
- Open the Applications folder, go into the Utilities folder, and open the Terminal program
- Use "cd" command to change the working directory to the folder where you saved the .py file and the input files (demo.psv and events.psv) (e.g., cd Documents/Lumiata/).
- Type "python ./Kapralov_Sasha.py" to run the program.

If running from a Jupyter notebook on Mac:
- Open the Applications folder, go into the Utilities folder, and open the Terminal program
- Use "cd" command to change the working directory to the folder where you saved the .ipynb file and the input files (demo.psv and events.psv).
- Type "jupyter notebook" and press Enter
- Open the Kapralov_Sasha.ipynb file and from the Cell menu select "Run All"

Testing:

The "Kapralov_Sasha_testing.py" script can be used to test the full program.  It uses the demo_testing.psv and events_testing.psv files as input.  Those files are truncated versions of the full demo.psv and events.psv files and can be modified further to test different data scenarios.  The output file is patients_testing.json.
