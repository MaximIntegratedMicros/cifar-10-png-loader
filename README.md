# Draft Instructions

## Preparing the MAX78000EVKIT board
* Build and load the program 'cifar-10-auto-test' on the MAX78000 EVKIT/Feather board: https://github.com/MaximIntegratedAI/MaximAI_Documentation/blob/master/MAX78000_Evaluation_Kit/README.md#building-the-sdk-examples


## Preparing the host machine
(Skip any step where requirement is already met)
1. Install Python 3.7 or 3.8. Python 2.x and 3.9 are incompatible.
2. Install pip: https://pip.pypa.io/en/stable/installing/
3. Install and create the virutal environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv
4. Clone the github repository: `$ git clone <link_to_repo>`
5. Navigate to the repository: `$ cd <repo_name>`
6. Activate the virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment
7. Install the requirements for this project: `$ pip install -r requirements.txt`
8. Open the file main.py in a code editor and change the 'serial_dev' variable if required.
8. Store the test images in 32x32 RGB .png format in a directory.
9. Make sure the MAX78000EVKIT is powered on and running the 'cifar-10-auto-test' example, then run the python script: `$ python main.py <path_to_test_images>`

### Expected Output
file1.png - Class:0

file2.png - Class:9
