# Tendable app automation

### (with Python+Selenium+pytest/allure)

----


An Automation project for UI automation of application. The project developed with python using selenium webdriver.
The reporting tools used are optional, either allure or pytest-html-reporter may used or reporting purpose with
different execution commands


### **Pre-requisites**

* [Python](https://www.python.org/downloads/)
* [Install NodeJS and NPM](https://nodejs.org/en/download/)
* [Python interpreter](https://www.python.org/downloads/release/python-3114/) 3.12 or higher


-------
### Installing Dependencies

* Unzip and navigate to the project folder.

* upgrade the pip with terminal 
	
		pip3 install --upgrade pip

`OR`

        python.exe -m pip install --upgrade pip
	
* install dependencies as follows

		pip3 install -r requirements.txt

### Test data:
Test data used in execution are mainly coming from static and dynamic sources, the static test data is 

will pull be from '/Test_Data' folder. [test_data.py](Test_Data/test_data.py) file store all the test data required for execution.

Whereas dynamic test data will be generated at runtime and pushed to the test case from [TestDataGenerator](Utils/TestDataGenerator.py) file.

### Browser Mode:

* Update the [**.env**](.env) file with browser mode (for Headless execution) else the execution will run as 'Headed' by default.

        BROWSER=chrome-headless

* Note: the application is not rendering responsively for headless mode. it renders in [mobile view](zz_HeadlessViewAppPage/test_TCID_002_verify_top_level_menus.png) when executed in headless mode.

### Running The Tests:

* Update the [**.env**](.env) file with url parameters and save the file.

        URL=

* To execute tests, run following command.

```commandline
    pytest
```
 - if above command not working (depending on system path setup for python) following command may be used to run the suite

```commandline
    python -m pytest
```
        
    
* To execute individual test, run following command.

        pytest src/testsuite/TestModule1_Home/test_tendable_home.py

* To execute tests from individual test folders, run following command.

        pytest src/testsuite/TestModule1_Home

### Reports:
    

* *pytest-html-reports*: Reports will be generated at the dir level from the  test executed, if executed from project root, report can be accessed here
 [report/pytest_html_report.html](report/pytest_html_report.html)


### Troubleshooting

#### for allure 

if allure not working
execute following command in command line using [npm](https://www.npmjs.com/package/allure-commandline)

```commandline
npm install -g allure-commandline --save-dev
```
---



