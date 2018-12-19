# README for sakhacabs
(kindly install Xetrapal first)
==

## Prerequisites:


'''python
mongod (community edition)
apache2
xetrapal
'''

## first clone the repository to your system :

git clone https://github.com/hackegram/sakhacabs


## install the dependencies:

cd sakhacabs/
sudo -H pip install -r requirements.txt
sudo -H pip install configparser
sudo -H pip install oauth2client


create the symbolic link of the file in /opt directory:

sudo ln -s /home/username/sakhacabs /opt/sakhacabs


copy the folder sakhacabs-appdata to /opt:


edit the config files of the sakhacabs-appdata and make the changes:

/opt/sakhacabs-appdata in place of /home/arjun/sakhacabs 


now, create the symbolic link of the file bookingweb:

sudo ln -s /opt/sakhacabs/bookingweb /var/www/html/bookingweb


Now deploy the ip address:

cd /home/username/sakhacabs
 sh deploy.sh 192.168.56.101  your IP address
 

Now, go to sakhacabs and run the dispatcher:

cd /home/username/location/sakhacabs
python dispatcherapi.py




