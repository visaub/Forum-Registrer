# Forum Registrer

App that can be used for the check in of attendances on big events with many activities. It includes a QR scanner. Credit most be given to <a href="https://github.com/HackAssistant/registration">HackAssistant</a> and <a href="https://github.com/jandrikus">Jandrikus</a>.

For deploying this web-app it is highly recommended to use <a href='https://www.pythonanywhere.com'> pythonanywhere</a>, because it the easiest platform to use.

<h3> Starting </h3>

Create an account with any username, open a BASH console and paste the following line:

<code> git clone https://github.com/visaub/Forum-Registrer && cd Forum-Registrer</code>

Then, go to the 'Web' tab and create a new webapp using Flask and Python3. The application is located at the script forum_app.py. The 'Source Code' and 'Working directory' must point to the folder where forum_app.py is located.

<h3> Custom </h3>

Feel free to edit the templates, add your logo, change the CCS and customize anything you want.

<h3> Add Assistants, Activities and Volunteers </h3>

Upload the three documents with these exact names on the 'data' folder:
- Cens.csv 
- Acts.csv
- Colabs.csv

Cens.csv contains the Name, First Surname and Second Surname of all the people that can attend your events.
Acts.csv is a file with the activities. The structure is the following: 'Kind of activity;Name of Activity;Start time;End time;counts'. counts is a bool (0 or 1), if (counts == 1) then the duration of the activity is added up to the number of hours a person has completed
Colabs.csv holds the information of the volunteers, 'Username;Password;Name;is_admin'. The username and password are requiered to login on the platform. is_admin == 1 allows the user to access more menus and log people in on all activities, whereas a regular user (is_admin == 0) can only see the activities that take place at that moment.

It is very important that these three files contain correct and complete information.
Load the information going to forum_app.py, hitting RUN and typing <code>reset()</code> on the command prompt that pops up.
After this step it is not possible to add new People, Activities or Volunteers to the app, nor to modify the ones loaded, so only reset when you are sure the information is correct. (On future this will be fixed.)

<h3>And you are ready to go!</h3>

Note: to use camera to scan the QR code of the UPC ID the server must be able to access https://identitatdigital.upc.edu. On pythonanywhere that is only possible with an upgraded account, with prices starting at 5 $/month.

It is recommended to read the user guide (now in Spanish). 

Finally, after your event is over, you can download a .csv with the number of hours and activities each participant took. Log in as an admin and type on the address bar your webpage followed by /reset.

<b>Enjoy!</b>