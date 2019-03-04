# This code is for installation on pythonanywhere

# PATH virtualenv = /home/forum/.virtualenvs/myenv36
# PATH wsgi = var/www/forum_pythonanywhere_com_wsgi.py

from forum_app import initDB_colabs, initDB_alums, initDB_acts, LoadDataBase, data_path
import os
import sys
import platform

current_user=os.environ.get('USER')
if current_user==None:
    current_user='DOESNT_MATTER_BECAUSE_NOT_USED'
wsgi_file="""
import sys
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/myenv36')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
#
## The "/home/forum" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/forum/myproject"

current_user=os.environ.get('USER')
print(current_user)
path = '/home/"""+current_user+"""/Forum-Registrer/web'
if path not in sys.path:
    sys.path.append(path)
from forum_app import app as application  # noqa
"""


def reset():
    f=open(data_path+'/log.txt','w');
    f.write('');f.close()
    ddbb=LoadDataBase()
    if os.path.isfile(ddbb):
        os.remove(ddbb)
    initDB_colabs()
    initDB_alums()
    initDB_acts()
    print('Success. The database was initialized with the information stored on the .csv files')
    #return render_template('text.html',title='Success', message='The database was initialized with the information stored on the .csv files')


def write_new_wsgi():
	current_user=os.environ.get('USER')
    if current_user==None:
        current_user='DOESNT_MATTER_BECAUSE_NOT_USED'
	print('Current user: '+current_user)
	#print("Hello people, it's me. ")
    #domain=input("Are you going to use: ")
	path_wsgi='/var/www/'+current_user+'_pythonanywhere_com_wsgi.py'
	f=open(path_wsgi,'w')
	f.write(wsgi_file)
	f.close()
	print('Success. WSGI file generated')

if __name__=='__main__':
    reset()
    if 'Windows' not in platform.platform():
        write_new_wsgi()   #like:  var/www/forum_pythonanywhere_com_wsgi.py

