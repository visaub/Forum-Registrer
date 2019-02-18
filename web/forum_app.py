import sqlite3
import time
import unidecode
from datetime import datetime
import os
import requests
from flask import Flask, render_template, request, redirect, abort, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from functools import wraps
from bs4 import BeautifulSoup as soup

from config import margin, time_change

def get_info(url):
    r=requests.get(url)
    page_html=r.text
    page_soup=soup(page_html,'html.parser')
    taules=page_soup.findAll('table')
    tds_1=taules[0].findAll('td')
    nom=tds_1[1].text
    unitat_1=tds_1[5].text
    usuari=str(tds_1[7]).split('<')[1].split('>')[1]
    domini=str(tds_1[7]).split('>')[2].split('<')[0]
    correu_1=usuari+'@'+domini
    llista_correus=[correu_1]
    llista_unitats=[unitat_1]
    if len(taules)>2:
        for t in range(1,len(taules)-1):
            tds_t=taules[t].findAll('td')
            unitat_t=tds_t[3].text
            llista_unitats.append(unitat_t)
            usuari=str(tds_1[7]).split('<')[1].split('>')[1]
            domini=str(tds_1[7]).split('>')[2].split('<')[0]
            correu_t=usuari+'@'+domini
            llista_correus.append(correu_t)
    #print(nom);print(llista_correus);print(llista_unitats)
    return (nom,llista_unitats,llista_correus)

app = Flask(__name__)
data_path=os.path.abspath('data')

### Login ###

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userID):
    return Colab(userID=userID)

app.config.update(
    DEBUG = False,
    SECRET_KEY = 'IM_A_SECRET_U_CANT_SEE_ME. Victor wapo'
)

def act_valid_required(f):
    @wraps(f)
    def inner2(*args, **kwargs):
        try:
            if current_user.is_authenticated and act_valid(current_user.actual):
                return f(*args, **kwargs)
            else:
                return render_template('text.html', message='Activity not available for registration', title='Not allowed')
        except AttributeError:
            return redirect(url_for('pau'))
    return inner2

def login_required(f):
    @wraps(f)
    def inner2(*args, **kwargs):
        try:
            if current_user.is_authenticated:
                return f(*args, **kwargs)
            else:
                return redirect('/')
        except AttributeError:
            return redirect(url_for('pau'))
    return inner2

def admin_required(f):
    @wraps(f)
    def inner2(*args, **kwargs):
        try:
            if current_user.is_authenticated and current_user.admin:
                return f(*args, **kwargs)
            else:
                title='Not organizer'
                message='Sorry, you are not allowed to see this content. Please apply for organizer and try again next year.'
                return render_template('text.html',title=title,message=message)
        except AttributeError:
            return redirect(url_for('pau'))
    return inner2

### Users and databases ###

class Alum():
    def __init__(self, userID = 0, unif = ''):
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        if userID:
            self.__dict__['userID'] = userID
            curs.execute('SELECT * FROM alums WHERE userID=?', (userID,))
        elif unif:
            self.__dict__['unif'] = unif
            curs.execute('SELECT * FROM alums WHERE unif=?', (unif,))
        try:
            user = curs.fetchone()
            l=len(user)
            self.__dict__['userID'] = int(user[0])  #INTEGER
            self.__dict__['unif'] = str(user[1])    #TEXT
            self.__dict__['name'] = str(user[2])    #TEXT
            self.__dict__['surname'] = str(user[3]) #TEXT
            for i in range(4,l,2):
                self.__dict__['act{0}'.format(int((i-4)/2+1))] = user[i]        #INTEGER
                self.__dict__['date_act{0}'.format(int((i-4)/2+1))] = user[i+1] #FLOAT
            conn.commit()
            conn.close()
        except StopIteration:
            conn.commit()
            conn.close()
            return abort(401)
    def __repr__(self):
        return self.name+', '+self.surname+' = '+self.unif
    def get(self, key):
        return self.key
    def __setattr__(self, key, value):
        self.__dict__[key] = value
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE alums SET {0}=? WHERE userID=?'.format(key), (value, self.userID))
        conn.commit()
        conn.close()
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except sqlite3.OperationalError:
            return 'jajaja'
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE alums SET {0}=? WHERE userID=?'.format(key), (value, self.userID))
        conn.commit()
        conn.close()
    def get_id(self):
        return self.userID

class Act():
    def __init__(self, actID = 0):
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        if actID:
            self.__dict__['actID'] = actID
            curs.execute('SELECT * FROM acts WHERE actID=?', (actID,))
        try:
            user = curs.fetchone()
            self.__dict__['actID'] = user[0]        #INTEGER
            self.__dict__['kind'] = user[1]         #TEXT
            self.__dict__['name'] = user[2]         #TEXT
            self.__dict__['begin'] = user[3]        #FLOAT
            self.__dict__['end'] = user[4]          #FLOAT
            self.__dict__['counts'] = user[5]       #BOOL
            conn.commit()
            conn.close()
        except StopIteration:
            conn.commit()
            conn.close()

    def __repr__(self):
        return self['name']
    def get(self, key):
        return self.key
    def __setattr__(self, key, value):
        self.__dict__[key] = value
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE acts SET {0}=? WHERE actID=?'.format(key), (value, self.actID))
        conn.commit()
        conn.close()
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return False
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE acts SET {0}=? WHERE actID=?'.format(key), (value, self.actID))
        conn.commit()
        conn.close()
    def get_id(self):
        return self.actID

class Colab(UserMixin):
    def __init__(self, userID = 0, email = ''):
        if userID:
            conn = sqlite3.connect(LoadDataBase())
            curs = conn.cursor()
            curs.execute('SELECT * FROM colabs WHERE userID=?', (userID,))
            try:
                user = curs.fetchone()
                conn.commit()
                conn.close()
                self.__dict__['userID'] = user[0]
                self.__dict__['email'] = user[1]
                self.__dict__['password'] = user[2]
                self.__dict__['name'] = user[3]
                self.__dict__['admin'] = user[4]
                self.__dict__['actual'] = user[5]
            except StopIteration:
                conn.commit()
                conn.close()
                return abort(401)
        elif email:
            conn = sqlite3.connect(LoadDataBase())
            curs = conn.cursor()
            curs.execute('SELECT * FROM colabs WHERE email=?', (email,))
            try:
                user = curs.fetchone()
                conn.commit()
                conn.close()
                self.__dict__['userID'] = user[0]
                self.__dict__['email'] = user[1]
                self.__dict__['password'] = user[2]
                self.__dict__['name'] = user[3]
                self.__dict__['admin'] = user[4]
                self.__dict__['actual'] = user[5]
            except StopIteration:
                conn.commit()
                conn.close()
                return abort(401)
    def __repr__(self):
        return self['name']
    def get(self, key):
        return self[key]
    def __setattr__(self, key, value):
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE colabs SET {0}=? WHERE userID=?'.format(key), (value, self.userID))
        conn.commit()
        conn.close()
    def __getitem__(self, key):
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute(f'SELECT {key} FROM colabs WHERE userID=?', (self.userID,))
        try:
            user = curs.fetchone()
            conn.commit()
            conn.close()
            return user[0]
        except StopIteration:
            conn.commit()
            conn.close()
            return False
    def __setitem__(self, key, value):
        conn = sqlite3.connect(LoadDataBase())
        curs = conn.cursor()
        curs.execute('UPDATE colabs SET {0}=? WHERE userID=?'.format(key), (value, self.userID))
        conn.commit()
        conn.close()
    def get_id(self):
        return self.userID

def load_alums():
    f=open(data_path+'/cens.csv','r',encoding='utf-8')#
    s=f.read();f.close()
    if ';' in s:
        sep=';'
    elif ',' in s:
        sep=','
    elif '\t' in s:
        sep='\t'
    else:
        raise ValueError("the separator must be either '\t', ';' or ','")
    ls=s.split('\n')
    matches=[];
    for e in ls[1:]:
        if len(e.split(sep))>2:
            le=e.split(sep)
            matches.append(le)
    return matches

def load_colabs():
    f=open(data_path+'/colabs.csv','r',encoding='utf-8')
    s=f.read();f.close()
    if ';' in s:
        sep=';'
    elif ',' in s:
        sep=','
    elif '\t' in s:
        sep='\t'
    else:
        raise ValueError("the separator must be either '\t', ';' or ','")
    l=s.split('\n')
    ll=[]
    for e in l[1:]:
        if len(e.split(sep))>2:
            ll.append(e.split(sep))
    return ll

def load_acts():
    f=open(data_path+'/acts.csv','r',encoding='utf-8')
    s=f.read();f.close()
    if ';' in s:
        sep=';'
    elif ',' in s:
        sep=','
    elif '\t' in s:
        sep='\t'
    else:
        raise ValueError("the separator must be either '\t', ';' or ','")
    l=s.split('\n')
    ll=[]
    for e in l[1:]:
        if len(e.split(sep))>2:
            ll.append(e.split(sep))
    return ll

#@app.route('/init_alums')
def initDB_alums():
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('CREATE TABLE alums (userID INTEGER PRIMARY KEY, unif TEXT, name TEXT, surname TEXT)')
    conn.commit()
    conn.close()
    matches = load_alums()
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    for match in matches:
        name, surname1, surname2 = match
        add_alum(name,surname1,surname2)
    conn.commit()
    conn.close()
    #return render_template('text.html', title='Success', message='Alums initiated')

def add_alum(name,surname1,surname2):
    surname=surname1+' '+surname2; name=name.title(); surname=surname.title()
    unif=uniform(name+surname)
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('INSERT INTO alums (unif, name, surname) VALUES (?,?,?)', (unif, name, surname))
    conn.commit()
    conn.close()

#@app.route('/init_colabs')
def initDB_colabs():
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    conn.commit()
    curs.execute('CREATE TABLE colabs (userID INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT, password TEXT, admin BOOL, actual INTEGER)')
    conn.commit()
    conn.close()
    colabs = load_colabs()
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    for colab in colabs:
        email, password, name, admin = colab
        try:
            curs.execute('INSERT INTO colabs (email, password, name, admin, actual) VALUES (?,?,?,?,?)', (email, name, password, admin, 0))
        except sqlite3.IntegrityError:
            mensaje = 'ERROR IN COLABS'
            print(mensaje)
    conn.commit()
    conn.close()
    #return render_template('text.html', title='Success', message='Colabs initiated')

def add_act_to_alums(i):
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('ALTER TABLE alums ADD act{0} INTEGER'.format(i))
    curs.execute('ALTER TABLE alums ADD date_act{0} FLOAT'.format(i))
    curs.execute('UPDATE alums SET act{0}=0'.format(i))
    curs.execute('UPDATE alums SET date_act{0}=0'.format(i))
    conn.commit()
    conn.close()
    f=open(data_path+'/logs/act{0}.txt'.format(i),'w',encoding='utf-8')
    f.close()

#@app.route('/init_acts')
def initDB_acts():
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    conn.commit()
    curs.execute('CREATE TABLE acts (actID INTEGER PRIMARY KEY, kind TEXT, name TEXT, begin FLOAT, end FLOAT, counts BOOL)')#, duration FLOAT)')
    conn.commit()
    conn.close()
    acts = load_acts()
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    for act in acts:
        kind, name, date_begin, date_end, counts = act
        begin=time.mktime(datetime.strptime(date_begin,'%Y/%m/%d %H:%M').timetuple())-time_change
        end=time.mktime(datetime.strptime(date_end,'%Y/%m/%d %H:%M').timetuple())-time_change
        try:
            curs.execute('INSERT INTO acts (kind, name, begin, end, counts) VALUES (?,?,?,?,?)', (kind, name, begin, end, counts))
        except sqlite3.IntegrityError:
            mensaje = 'ERROR WITH ACTS'
            print(mensaje)
    conn.commit()
    conn.close()
    for logfile in os.listdir(data_path+'/logs'):
        os.remove(data_path+'/logs/'+logfile)
    for i in range(1, len(acts)+1):
        add_act_to_alums(i)
    #return render_template('text.html', title='Success', message='Activities initiated')

### Functions ###

def LoadDataBase(ddbb='everything.sql'):
    return os.path.join(data_path,ddbb)

def uniform(name):
    n=name.strip(); n=n.upper(); n=unidecode.unidecode(n); n=n.replace(' ',''); n=n.replace('-','')
    return n

def valid(name):
    return len(uniform(name))>=3

def getmatches(unif):
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('SELECT * FROM alums WHERE unif LIKE ?', ('%'+unif+'%',))
    matches=curs.fetchall()
    conn.commit()
    conn.close()
    return matches

def cross(unif,actID):
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('SELECT * FROM alums WHERE unif = ?', (unif,))
    matches=curs.fetchall()
    conn.commit()
    conn.close()
    if len(matches)==0:
        return [False,'-1']
    ID=matches[0][0]
    alum=Alum(userID=ID)
    if alum['act{0}'.format(actID)]==True:
        return [False, '1', alum['date_act{0}'.format(actID)], alum.name+' '+alum.surname]
    else:
        alum['act{0}'.format(actID)]=True
        date=time.time()
        alum['date_act{0}'.format(actID)]=date
        return [True, '0', date, alum.name+' '+alum.surname]

def act_valid(actual):
    if current_user.admin:
        return True
    else:
        try:
            act_i=Act(actual)
            begin,end=act_i.begin,act_i.end
            t=time.time()
            return begin<t+margin and t<end+margin
        except TypeError:
            return False

def get_events():
    l_acts=[];i=1;err=False
    while not err:
        try:
            act_i=Act(i)
            if act_valid(i):
                l_acts.append(act_i)
            i+=1
        except TypeError:
            err=True
    d={}
    for act_i in l_acts:
        if act_i.kind not in d:
            d[act_i.kind]=[(act_i.name,act_i.actID)]
        else:
            d[act_i.kind].append((act_i.name,act_i.actID))
    return d


######### URLs #########


@app.errorhandler(401) # handle login failed
def unauthorized(e):
    title = '401 Error'
    message = 'Login failed'
    return render_template('text.html', title = title, message = message)

@app.errorhandler(404) # handle not found
def not_found(e):
    title = '404 Error'
    message = 'Page not found'
    return render_template('text.html', title = title, message = message)

@app.errorhandler(401) # handle login failed
def page_not_found(e):
    title = 'Uppps'
    message = 'Login failed'
    return render_template('text.html', title = title, message = message)

@app.route('/')
def index():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url)
    if current_user.is_authenticated:
        current_user.actual=0
        events=get_events()
        return render_template('index.html', name=current_user.name, events=events, yeah=False)
    return render_template('welcome.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            return abort(401)
        rememberMe = False
        if 'rememberMe' in request.form:
            rememberMe = bool(request.form['rememberMe'])
        try:
            user = Colab(email=email)
        except TypeError:
            title = 'Upps'
            message = 'This user does not exist.'
            return render_template('text.html', title = title, message = message)
        if str(user.password) == str(password):
            login_user(user,remember=rememberMe)
            current_user.actual=0
            events=get_events()
            return render_template('index.html', name=current_user.name, events=events, yeah=True)
        else:
            titulo = 'Upps'
            mensaje = 'Wrong password'
            return render_template('text.html', title = titulo, message = mensaje)
    else:
        return redirect(url_for('index'))

@app.route('/check-in',methods=['GET','POST'])
@login_required
@act_valid_required
def checkin():
    unif=request.args.get('id','nothing')
    if unif=='nothing':
        actID=current_user.actual
        if actID==0:
            return redirect('/')
        if request.method=='POST':
            name = str(request.form['name'])
            if valid(name):
                matches=getmatches(uniform(name))
                return render_template('search.html',matches=matches,name=name,act=Act(actID).name)
            return ('',204)
        else:
            return render_template('check-in.html', status='', event=Act(actID))
    actID=current_user.actual
    if actID==0:
        return redirect('/')
    status=cross(unif,actID)
    if status[0]==False:
        if status[1]=='1':
            status[2]=datetime.fromtimestamp(float(status[2])+time_change).strftime('%Y-%m-%d %H:%M:%S')
    elif status[0]==True:
        f=open(data_path+'/log.txt','a');
        f.write(status[3]+', '+Act(actID).name+', '+str(datetime.fromtimestamp(float(status[2])+time_change).strftime('%Y-%m-%d %H:%M:%S'))+'\n')
        f.close()
        f=open(data_path+'/logs/act{0}.txt'.format(actID),'a')
        f.write(status[3]+', '+str(datetime.fromtimestamp(float(status[2])+time_change).strftime('%Y-%m-%d %H:%M:%S'))+'\n')
        f.close()
    return render_template('check-in.html',status=status, event=Act(actID))


@app.route('/check-in/qr',methods=['GET','POST'])
@login_required
@act_valid_required
def qr():
    actID=current_user.actual
    if actID==0:
        return redirect('/')
    m=request.args.get('m','0')
    return render_template('qr.html',m=m)

@app.route('/check-in/read')
@login_required
@act_valid_required
def upc_id():       #not complete yet
    url_VS='https://identitatdigital.upc.edu/vid/MI0E4LO3JYKXFW'
    url=str(request.args.get('q','nothing'))
    print(url)
    f=open(data_path+'/url_qr.txt','a')
    f.write(url+'\n');f.close()
    if url=='nothing' or url[:37]!='https://identitatdigital.upc.edu/vid/':
        return redirect('/check-in/qr?m=1')
    try:
        nom,llista_unitats,llista_correus=get_info(url) #scrap_carnet.get_info(url)
    except all:
        return redirect('/check-in/qr?m=1')
    return redirect('/check-in?id='+uniform(nom))

@app.route('/paunotnow') #for testing porpouses
def pau():
    return render_template('pau.html')

@app.route('/log')
@login_required
def log():
    events=get_events();
    if current_user.admin or True: events['All people so far']=[('Master log',0)]
    return render_template('logs.html', name=current_user.name, events=events, yeah=False)

@app.route('/log/<int:actID>')
@login_required
def log_i(actID):
    if actID==0:
        f=open(data_path+'/log.txt','r');
        s=f.read();f.close()
        lalums=s.split('\n')[:-1]; lalums.reverse()
        c=len(s.split('\n'))-1
        if not current_user.admin:
            lalums=lalums[:min(len(lalums),20)]
        return render_template('log.html',lalums=lalums,act='All registrations',c=c,a=1)
    try:
        Act(actID)
    except TypeError:
        return render_template('text.html',message='This activity does not exist',title='Upss')
    if not act_valid(actID):
        return redirect('/log')
    f=open(data_path+'/logs/act{0}.txt'.format(actID),'r')
    s=f.read();f.close()
    lalums=s.split('\n')[:-1]; lalums.reverse()
    c=len(s.split('\n'))-1
    if not current_user.admin:
        lalums=lalums[:min(len(lalums),20)]
    return render_template('log.html',lalums=lalums,act='Students at: '+Act(actID).name,c=c,a=1)

@app.route("/logout", methods=["GET", "POST"])
def user_space_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/act/<int:set_next>')
@login_required
def act(set_next):
    try:
        Act(set_next)
    except TypeError:
        return render_template('text.html',message='This activity does not exist',title='Upss')
    current_user.actual=set_next
    if set_next>0:
        #if act_valid(set_next):
        return redirect('/check-in')
    else:
        return redirect('/')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html',title='About')

@app.route('/all/<kind>')   #to get activitites and volunteers
@login_required
def all_kinds(kind):
    d={'acts':'activities','colabs':'volunteers','cens':'students'}
    try:
        file=d[kind]
    except KeyError:
        return redirect('/')
    if kind!='acts':
        if not current_user.admin:
            return redirect('/')
    f=open(data_path+'/'+kind+'.csv')
    s=f.read();f.close()
    lacts=s.split('\n')[:-1]
    for i in range(len(lacts)):
        lacts[i]=' | '.join(lacts[i].split(';'))
    return render_template('log.html',lalums=lacts,act='All '+file)

@app.route('/hours') #/<word>')     #Download all hours. Requires a special word
@login_required
@admin_required
def sort_by_hours():
    #if word!='MI0E4LO3JYKXFW':  #This is a password I set
    #    message='Wrong password'
    #    title='Not authorized'
    #    return render_template('text.html',message=message,title=title)
    conn = sqlite3.connect(LoadDataBase())
    curs = conn.cursor()
    curs.execute('SELECT actID, counts, begin, end FROM acts')
    all_acts=curs.fetchall()
    conn.commit()
    conn.close()
    good_acts=[]
    for a in all_acts:
        if a[1]>0:
            good_acts.append(a[0])
    users=[]
    IDalum=1; keep_going=True
    while keep_going:
        try:
            alum_i=Alum(IDalum)
            lacts_alum_i=[]
            for actID in good_acts:
                if alum_i['act{0}'.format(actID)]:
                    a=Act(actID)
                    lacts_alum_i.append((a.begin,a.end))
            if len(lacts_alum_i)>0:
                lacts_alum_i.sort()
                h=0; b,e=lacts_alum_i[0]
                for i in range(1,len(lacts_alum_i)):
                    bi,ei=lacts_alum_i[i]
                    if bi>e:
                        h+=e-b
                        b,e=bi,ei
                    else:
                        e=ei
                h+=e-b
                users.append((alum_i.name,alum_i.surname,h/3600,len(lacts_alum_i)))
            IDalum+=1
        except TypeError:
            keep_going=False
    users.sort(reverse=True)
    s='Name\tSurname\tHours\tActivities\n'
    for user in users:
        name,surname,hours,n_acts = user
        s+=name+'\t'+surname+'\t'+str(hours)+'\t'+n_acts+'\n'
    f=open(data_path+'/total.csv','w',encoding='utf-16')
    f.write(s);f.close()
    title='Aquí teniu tot'
    message='La feina de setmanes i centenars de fulls reduïda a un parell de clics'
    return send_file(data_path+'/total.csv', as_attachment=True)
    return [render_template('text.html',message=message,title=title),send_file(data_path+'/total.csv', as_attachment=True)]

