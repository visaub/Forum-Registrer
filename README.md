# Forum Registrer

App that can be used for the check in of attendances on big events with many activities. It includes a QR scanner. Credit must be given to <a href="https://github.com/HackAssistant/registration">HackAssistant</a> and <a href="https://github.com/jandrikus">Jandrikus</a>.

For deploying this web-app it is highly recommended to use <a href='https://www.pythonanywhere.com'> pythonanywhere</a>, because it the easiest platform to use.

## Starting

Create an account with any username, open a BASH console and paste the following lines:

- `git clone https://github.com/visaub/Forum-Registrer`
- `cd Forum-Registrer`
- `mkvirtualenv myenv36 --python=/usr/bin/python3.6`
- `workon myenv36`
- `bash install_libraries.sh`

Then, go to the 'Web' tab and create a new webapp, using 'Manual Configuration' and 'Python 3.6'. The application is located at the script forum_app.py. The 'Source Code' and 'Working directory' must point to the folder where **forum_app.py** is located, usually the path is '/home/**your_pythonanywhere_username**/Forum-Registrer/web/'. On 'Virtualenv', you have to write `myenv36`, because it is the Virutal Environment that was created before and will host the app.

### Custom

Feel free to edit the templates, add your logo, change the CCS and customize anything you want.

## Add Participants, Activities and Volunteers to the database (required)

Upload the three documents with these <b>exact</b> names on the 'data' folder:

- **Cens.csv** (Participants)

- **Acts.csv** (Activities)

- **Colabs.csv** (Volunteers)

All files have to include their respective headers.

### Participants
_Cens.csv_ contains the Name, First Surname and Second Surname of all the people that can attend your events.

Header: **Name;First_family_name;Second_family_name**


### Activities

Acts.csv is a file with the activities. 

Header: **Kind of activity;Name of Activity;Start time;End time;counts**. 
_counts_ is a bool (0 or 1), if `(counts == 1)` then the duration of the activity is added up to the number of hours a person has completed.

### Volunteers

_Colabs.csv_ holds the information of the volunteers. 

Header:**Username;Password;Name;is_admin**

The username and password are requiered to login on the platform. `is_admin == 1` allows the user to access more menus and log people in on all activities, whereas a regular user `(is_admin == 0)` can only see the activities that take place at that moment.

It is very important that these three <b>.csv</b> files contain correct and complete information. An example of these files could be found <a href='https://github.com/visaub/Forum-Registrer/tree/master/web/EXAMPLES'> on this link </a>.

Load the information oppening the console on the <b>/Forum-Registrer/web/</b> directory and running:

`workon myenv36`
`python reset.py`

After this step it is not possible to add new People, Activities or Volunteers to the app, nor to modify the ones loaded, so only reset when you are sure the information is correct. (On the future this feature will be included.)

After that, you must reload the webapp, by going to the 'Web' tab and clicking Reload.

### And you are ready to go!

Note: to use camera to scan the QR code of the UPC ID the server must be able to access https://identitatdigital.upc.edu. On pythonanywhere that is only possible with an upgraded account, with prices starting at 5 $/month.

It is recommended to read the user guide (now in Spanish). 

Finally, after your event is over, you can download a .csv with the number of hours and activities each participant took. Log in as an admin and type on the address bar your webpage followed by `/hours`.

## **Enjoy!**