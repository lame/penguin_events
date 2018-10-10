## Setting up ENV

To run the program, I recommend installing python3.7 and a virtual
environment to the project directory

    python3 -m venv env
    source env/bin/activate

Update pip and install the required pip packages

    pip install --upgrade pip
    pip install -r requirements.txt

## Running the Program

Then, simply run the program and provide an input file

    python3 main.py {input file}

## Running Tests

Specify the test file that you want to run as follows

    python3 -m unittest tests/models/vehicle_test.py
