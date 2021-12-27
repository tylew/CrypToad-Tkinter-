# "CRYPTOADZ" NFT PRICE ANALYSIS PROGRAM/DATABSE
### BY Tyler Lewis & Aviv Zohman
### @ Chapman Univ.

### Save some time, watch the [DEMO VIDEO](https://www.dropbox.com/s/a6uacp1kidlhtpm/CrypToadz%20TKinter%20Demo.mp4?dl=0)

## About
Final project for CPSC 408: Database Management
If you would like to re-create this project, you must install the following libraries and connect to a database with tables and entities which are laid out in SQL file included with this project.

If you decide to re-create our database, which will also make sure all data is up to data, file *createDatabase.py* can be used. Make sure to fill in your databases credentials within the file.

Else, here are the credentials to our pre-built database (STATIC DATABASE & NOT MAINTAINED):
  host = "34.132.124.28",
  user = "tyler",
  password = "rooter",
  database = 'finalproject'

## TO RUN
### Complete the following fix & library installs:
**Certification Quick Fix (First solution on page):**
  https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

**Libraries to install (MacOS):**
tkinter:
  * pip install tk

FPDF:
  * python setup.py install 

PIL:
  * python3 -m pip install --upgrade pip
  * python3 -m pip install --upgrade Pillow

urllib:
  * pip install urllib.request

connector:
  * pip install mysql-connector-python

**Start program (GUI folder):** 

  * python3 frame.py
