##Police_Management_System (DBMS Project)
A database for Police created using Django Framework , where the policemen can review all civilians's database and the criminal database.Also a civilian has the functionality to review a police station, fetch some details from the list of police stations and complaint against policemen which will be reviewed later by their senior officials.
###Steps to run project:
1. Download django 1.9.
2. use git clone ``` https://github.com/amanmj/Police_Management_System/ ```
3. change your password to your mysql database password in settings.py.
4. create a database named 'POLICE' through mysql.
5. change your path to the project's directory and create a superuser using ```python manage.py createsuperuser```
6. now run ``` python manage.py runserver```
6. open ```localhost:8000/admin``` and add a few police stations from there and log out.
7. now open the home page and browse ```localhost:8000```

<br>
##Browse through a list of police stations
![Alt Text](https://github.com/amanmj/Police_Management_System/blob/master/screenshots/Screenshot%20from%202016-04-24%2000-50-43.png)
<br>
##Review police stations when logged in from a civilian's account
![Alt Text](https://github.com/amanmj/Police_Management_System/blob/master/screenshots/Screenshot%20from%202016-04-24%2001-06-40.png)
<br>
##Complaint against a policeman
![Alt Text](https://github.com/amanmj/Police_Management_System/blob/master/screenshots/Screenshot%20from%202016-04-24%2001-07-33.png)

##Edit your personal details
![Alt Text](https://github.com/amanmj/Police_Management_System/blob/master/screenshots/Screenshot%20from%202016-04-24%2001-10-33.png)

##View a civilian's details, make him a criminal, view user/criminal database through policeman's account. Also view your junior policeman's account!
![Alt Text](https://github.com/amanmj/Police_Management_System/blob/master/screenshots/Screenshot%20from%202016-04-24%2001-11-27.png)
