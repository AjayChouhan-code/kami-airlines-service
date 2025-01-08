# KAMI Airlines Service

The KAMI Airlines Service is a Python-based solution designed to address the aircraft passenger capacity issue for KAMI Airlines. It includes functional code with simple setup and execution instructions to solve the passenger booking and capacity problem.

### Purpose
* Address the challenge of managing passenger capacity on flights for KAMI Airlines.
* Provide a solution that allows easy handling of bookings and passenger assignments.

### Local Dev Setup

# SetUp MySQL on your local machine with the help of the following commands.
* Run `$ sudo apt update` to update package indexes.
* Run `$ sudo apt install mysql-server` to install MySQL.
* Run `$ sudo systemctl status mysql` to verify that MySQL is installed successfully.
* You can also check the MySQL version with `$ mysql -v`.

### Steps to install and run KAMI Airlines Service on your local machine
* Run `$ pip install virtualenv` to install virtual environment.
* Run `$ virtualenv env -p python3.11` to create a virtual environment.
* Run `$ source env/bin/activate` to activate the virtual environment.
* Run `$ git clone git@github.com:your-username/kami-airlines-service.git` to clone the project repository.
* Run `$ cd kami-airlines-service` to enter the project directory.
* Run `$ pip install -r requirements.txt` to install the project dependencies.
* Run `$ python manage.py runserver` to start the project on your local machine.

### Running the Tests
* Run `$ cd kami-airlines-service` to enter the project directory.
* Run `$ python manage.py test kami_airlines_service/tests` to execute all test cases.

### Running Test Coverage
* Run `$ cd kami-airlines-service` to enter the project directory.
* Run `$ coverage run --source kami_airlines_service manage.py test` to run test cases with coverage.
* Run `$ coverage html` to view the test coverage results.

