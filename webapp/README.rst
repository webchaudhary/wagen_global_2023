Instructions
=============

* In a new system (Only tested in Ubuntu server) install the following software

  * PostgreSQL and its developing package
  * PostGIS
  * GRASS GIS
  * redis
  * git
  * GDAL software 
  * Apache
  * Virtualenv
  * Compilers
  * Python3 devel packages


**Install following packages**

Open a terminal and use following commands to install required libraries.

``sudo apt-get install git gdal-bin apache2 postgis redis-server virtualenv build-essential python3-dev libpq-dev pango1.0-tools``

``sudo apt-get install postgresql postgresql-postgis``

* Install grass gis using following commands

``sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable``

``sudo apt-get install grass grass-dev``

* Create a new grass location for wagen_global app

``grass -c EPSG:4326 -e /path/to/grassdata/wagen_global``

(Note that, in settings.py file "GRASS_DB" should be set as "/path/to/grassdata")

* Create an empty PostgreSQL database with PostGIS extension

``sudo -u postgres createuser wagen_global``

Open psql in the terminal using following command

``sudo -u postgres psql``

In the psql command:

| *# Change password of postgres user*
| ``ALTER USER postgres PASSWORD '*******';``
| ``ALTER USER wagen_global PASSWORD '********';``
| *# Give more privileges to user wagen*
| ``ALTER USER wagen_global WITH SUPERUSER;``
| *# quit psql*
| ``\q``

Create a new DB named "wagen_global":

| ``createdb -U YOURUSER -h YOURHOST wagen_global``
| ``psql -U YOURUSER -h YOURHOST wagen_global -c "CREATE EXTENSION postgis"``

* Download this source code and enter in directory wagen/webapp

* Create a Python 3 virtual environment in the webapp directory

``virtualenv -p /usr/bin/python3 venv``
``python3 -m venv venv``

* Activate the virtual environment

``source venv/bin/activate``

* Install dependencies with `pip`

``pip install -r requirements.txt``

* Set connection to the database and create its structure

  ```bash
  cd wagen
  cp wagen/template_settings.py wagen/settings.py
  # add user, password and grass settings in wagen/settings.py

  `python manage.py makemigrations webapp``
  `python manage.py migrate``
  `python manage.py collectstatic`

  # create a new user to access the features of web app
  python manage.py createsuperuser --username admin
  # to see the help
  python manage.py help
  ```


* The first time you run the webapp in the admin page (in testing mode is http://127.0.0.1:8000/admin),
  go to "sites" tab on left panel and Change the Domain name to the
  domain where the webapp is hosted. In case of localhost, change to 127.0.0.1:8000.
  The report will not adapt the template unless this change is made.

=============
TESTING
=============

* Start celery worker to use asynchronous requests

  `celery -A wagen worker -l INFO`

* At this point you could run the app

  `python3 manage.py runserver`

*run this to access on other device too

  `python manage.py runserver 0.0.0.0:8000`

* After running this you can access the dashboard on otherdevice too at "http://10.37.129.2:8000/"


* Open web browser at http://127.0.0.1:8000/



=============
DEPLOYMENT
=============
* Create all the stuff needed to run celery in deployment mode

  ```bash
  # create the pid directory
  `sudo mkdir /var/run/celery/`
  `sudo chown -R aman:aman /var/run/celery/`

  # copy the systemd configuration file
  `ln -s /home/aman/wagen_global/webapp/wagen/celery_wagen_global.service /etc/systemd/system`
  .. sudo ln -s /home/aman/wagen_global/webapp/wagen/celery_wagen_global.service /etc/systemd/system


.. EnvironmentFile=-/home/aman/wagen_global/webapp/wagen/celery.conf
.. WorkingDirectory=/home/aman/wagen_global/webapp/wagen/

  # modify the environment file if needed 
  # (for example the timeout for a single job set to 3000 seconds or number of concurrency set to 8)

  # reload the systemd files (this has been done everytime celery_wagen_global.service is changed)
  `sudo systemctl daemon-reload`
  # enable the service to be automatically start on boot
  `sudo systemctl enable celery_wagen_global.service`
  ```

* Start the celery app

  
  sudo systemctl start celery_wagen.service
  # to look if everything is working properly you can

  sudo systemctl status celery_wagen.service

  ls -lh /home/wagen/wagen/log/celery/
  .. ls -lh /home/aman/wagen_global/webapp/wagen/log/celery/

  
  tail -f /home/wagen/wagen/log/celery/worker1.log
  .. tail -f /home/aman/wagen_global/webapp/wagen/log/celery/worker1.log

  

* Copy the template `ini` file and modify the paths

  ```bash
  cp wagen/template_wagen.ini wagen/wagen.ini
  ```

* Copy the template Apache configuration file and modify it, specially the path

  ```bash
  sudo cp wagen/template_apache.conf /etc/apache2/sites-available/wagen.conf
  ```
* Install uwsgi python package in the venv
  (install it in the virtualenv environment)

* Install uwsgi libapache in the ubuntu system

  `sudo apt install libapache2-mod-uwsgi`

* Enable uwsgi and ssl module in apache

  `sudo a2enmod uwsgi`
  `sudo a2enmod ssl`

* Run the Django app using `uwsgi`
  (first, enable virtualenv environment)
  `uwsgi --ini wagen_global.ini`


* Activate the Apache configuration file
  `sudo a2ensite wagen.conf`
  `sudo systemctl restart apache2`




`sudo systemctl start celery_wagen_global.service`
`uwsgi --ini /home/aman/wagen_global/webapp/wagen/wagen_global.ini`




=================================================================
Restart the celery and uWSGI in development after updates
=================================================================


#Stop Celery Service
`sudo systemctl stop celery_wagen_global.service`

#Kill Remaining Celery Processes
`sudo pkill -9 -f 'celery worker'`

#Ensure All Processes Are Stoppedps aux | grep celery
`ps aux | grep celery`

# reload the systemd files (this has been done everytime celery_wagen.service is changed)
`sudo systemctl daemon-reload`


#Start Celery Service
`sudo systemctl start celery_wagen_global.service`

#Verify Celery is Running Correctly
`sudo systemctl status celery_wagen_global.service`


#Monitoring Logs
`tail -n 100 /home/aman/wagen_global/log/celery/worker1-7.log
tail -n 100 /home/aman/wagen_global/log/celery/worker1-6.log
tail -n 100 /home/aman/wagen_global/log/celery/worker1.log`

`tail -f /home/aman/wagen_global/log/celery/worker1-7.log`

`for file in /home/aman/wagen_global/log/celery/*.log; do
    echo "Checking $file"
    tail -n 20 $file
done`



# To stop uWSGI
`killall uwsgi`

#Restart uWSGI (first activate the venv)
`uwsgi --ini wagen_global.ini`



=============
Apache commands
=============


* Enable the virtual host with the following command:**
`sudo a2ensite global.waterinag.org.conf`

* To disable site**
(here global.waterinag.org.conf is apache conf file for global.waterinag.org website)
`sudo a2dissite global.waterinag.org.conf`


* Restart the Apache webserver to apply the changes:
`sudo systemctl reload apache2`
`sudo systemctl restart apache2`

* List all the enabled sites**
`ls -l /etc/apache2/sites-enabled`

* Test the apache configuration:**
`sudo apachectl configtest`


* Install certbot in Ubuntu (enable ssl certificate)
`sudo apt install certbot python3-certbot-apache`

* Set SSL and enable https**
`sudo certbot --apache -d global.waterinag.org`




=============
Possible errors
=============


# Check the socket file permissions after starting uWSGI:
`tail -f /home/aman/wagen_global/webapp/wagen/log/wagen_global.log`
`sudo tail -f /home/aman/wagen_global/webapp/wagen/log/wagen_global.log`

# If permission errors occurred

sudo chown -R www-data:www-data /home/aman/wagen_global/webapp/wagen
sudo chown -R aman:aman /home/aman/wagen_global/webapp/wagen/log/
sudo chmod -R 755 /home/aman/wagen_global/webapp/wagen/log/


# check uWSGI log
`tail -f /home/aman/wagen_global/webapp/wagen/log/wagen_global.log`


# check apache log if errors
`sudo tail -f /var/log/apache2/global_error.log`

# Ensure Apache Configuration Points to Correct Socket










sudo killall -9 uwsgi

sudo chown -R aman:aman /home/aman/wagen_global/webapp/wagen/
sudo chmod 755 /home/aman/wagen_global/webapp/wagen/

uwsgi --ini wagen_global.ini

tail -f /home/aman/wagen_global/webapp/wagen/log/wagen_global.log




