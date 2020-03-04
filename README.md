
<br>
<p align="center">
  <img alt="Logo Forum ETSEIB" src="https://raw.githubusercontent.com/visaub/Forum-Registrer/master/web/static/images/999981.png" width="10%"/>
</p>
<br>

# Forum Registrer






App that can be used to manage the check-in process of participants on fairs with many activities. 

Initially developed by **Forum ETSEIB** and used since 2018, https://forumetseib.upc.edu, the job fair for industrial engineering students at UPC, Barcelona. 

### Features:
- Import data from .csv files
- Volunteers and Organizers can check participants in to available activities. Volunteers have access limited to ongoing activities at the specific time, with a time window.
- Organizers are able to see complete information about participants and volunteers on a dashboard.
- Data of the attendance is exportable.
- Integrated QR scanner to read the code on UPC student ID, visit the URL and scrap the persons data, as an alternative to input the data.

For deploying this web-app it is highly recommended to use <a href='https://www.pythonanywhere.com'> pythonanywhere</a>, because it a platform easy to use and the development was done on it.

## Starting

Create an account with any username, open a BASH console and paste the following lines:

- `git clone https://github.com/visaub/Forum-Registrer`
- `cd Forum-Registrer`
- `mkvirtualenv myenv36 --python=/usr/bin/python3.6`
- `workon myenv36`
- `bash install_libraries.sh`

Then, go to the **Web** tab and create a new webapp, using _Manual Configuration_ and _Python 3.6_. The application is located at the script forum_app.py. The _Source Code_ and _Working directory_ must point to the folder where **forum_app.py** is located, usually the path is: 
-_/home/**your_pythonanywhere_username**/Forum-Registrer/web/_. 

On 'Virtualenv', you have to write `myenv36`, because it is the Virutal Environment that was created before and will host the app.

### Custom

Feel free to edit the templates, add your logo, change the CCS and customize anything you want on the `static` folder.

## Add Participants, Activities and Volunteers to the database (required)

Upload the three documents with these <b>exact</b> names on the 'data' folder:

- **cens.csv** (Participants)

- **acts.csv** (Activities)

- **colabs.csv** (Volunteers)

All files have to include their respective headers.
**Important**: the files must be saved with encoding **UTF-8**, otherwise pythonanywhere.com will not be able to read them.

### Participants
_cens.csv_ contains the Name, First Surname and Second Surname of all the people that can attend your events.

Header: **Name;First_family_name;Second_family_name**


### Activities

_acts.csv_ is a file with the activities. 

Header: **Kind of activity;Name of Activity;Start time;End time;counts**. 
_counts_ is a bool (0 or 1), if `(counts == 1)` then the duration of the activity is added up to the number of hours a person has completed. 

The times must follow the format: '%Y/%m/%d %H:%M' (examples: "2018/03/06 9:00", "2018/03/07 12:00").

### Volunteers

_colabs.csv_ holds the information of the volunteers. 

Header:**Username;Password;Name;is_admin**

The username and password are requiered to login on the platform. `(is_admin == 1)` allows the user to access more menus and log people in on all activities, whereas a regular user `(is_admin == 0)` can only see the activities that take place at that moment.

It is very important that these three <b>.csv</b> files contain correct and complete information. An example of these files could be found <a href='https://github.com/visaub/Forum-Registrer/tree/master/web/EXAMPLES'> on this link </a>.

Load the information oppening the console on the <b>/Forum-Registrer/web/</b> directory and running:

- `workon myenv36`
- `python reset.py`

After this step it is not possible to add new People, Activities or Volunteers to the app, nor to modify the ones loaded, so only reset when you are sure the information is correct. (On the future this feature will be included.)

After that, you must reload the webapp, by going to the 'Web' tab and clicking Reload.

### And you are ready to go!

Note: to use camera to scan the QR code of the UPC ID the server must be able to access https://identitatdigital.upc.edu. On pythonanywhere that is only possible with an upgraded account, with prices starting at 5 $/month.

It is recommended to read the user guide (now in Spanish). 

Finally, after your event is over, you can download a .csv with the number of hours and activities each participant took. Log in as an admin and type on the address bar your webpage followed by `/hours`.

## **Enjoy!**

Credit must be given to the team at <a href="https://hackupc.com">HackUPC</a> for the development of <a href="https://github.com/HackAssistant/registration">HackAssistant</a>, on which this project is inspired. Thanks also to Alejandro Alvarez, a.k.a. <a href="https://github.com/jandrikus">Jandrikus</a> and the rest of the team at <a href="https://sosetseib.upc.edu">Sos ETSEIB</a>.
