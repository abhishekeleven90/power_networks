# power_networks

Let's follow power elites.
Indian version of littlesis.org

sudo apt-get install python-django
sudo apt-get install python-mysqldb

ipython and django follow this:
sudo apt-get install python-django-extensions
http://codeispoetry.me/index.php/django-ipython-notebook-shell/
To fire ipython for a project: 
python manage.py shell_plus --notebook

bigautofield custom


##Scrapy
1. sudo su -
2. pip install scrapy


##FuzzyWuzzy
git clone git://github.com/seatgeek/fuzzywuzzy.git fuzzywuzzy
cd fuzzywuzzy
sudo python setup.py install
Also install: sudo apt-get install python-Levenshtein

#Keep this course! You have to do it!
https://github.com/amplab/datascience-sp14


##before summers

Installing git on <12.04: sudo apt-get install git-core

On the Japan Server the password for mysql is root.

Importing sql file: 
mysql -u root -p
create database powernetworks
source powernetworks.sql


linking to pyhton 2.6 DO NOT USE THIS :
rm /usr/local/bin/python
sudo ln -sf /usr/bin/python2.6 /usr/local/bin/python


django version:
python -c "import django; print(django.get_version())"

To remove django:
sudo apt-get purge python-django
