# README for sakhacabs
(kindly install Xetrapal first)
---

## Prerequisites:

[Mongod Community edition](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

[Apache2](https://linuxize.com/post/how-to-install-apache-on-ubuntu-18-04/)

[Xetrapal](https://github.com/suryaveer5320129/xetrapal)


## first clone the repository to your system :

```
git clone https://github.com/hackegram/sakhacabs

```

## install the dependencies:

```
cd sakhacabs/

sudo -H pip install -r requirements.txt
sudo -H pip install configparser
sudo -H pip install oauth2client
sudo -H pip install mongoengine flask-mongoengine
sudo -H pip install flask_restful flask_cors
```


## create the symbolic link of the file in /opt directory:


```sudo ln -s /home/username/sakhacabs /opt/sakhacabs```


## copy the file sakhacabs-appdata to /opt:

``` since the file sakhacabs-appdata contains some senstive data so it cant be shared on the repository, if you want to access the file you can mail me on gaursurya33@protonmail.com and listener@hackergram.org and file an issue here to let us know you've asked!```


## edit the config files of the sakhacabs-appdata and make the changes:

```/opt/sakhacabs-appdata in place of /home/arjun/sakhacabs``` 


## now, create the symbolic link of the file bookingweb:

```
sudo ln -s /opt/sakhacabs/bookingweb /var/www/html/bookingweb     
```

## now, create the symbolic link of the file sakhadispatcher:

   ```
   sudo ln -s /opt/sakhacabs/sakhadispatcher /var/www/html/sakhadispatcher
   ```
      
## Now deploy the ip address:

```cd /home/username/sakhacabs
   sh deploy.sh 192.168.56.101  <your IP address>
 ``` 

## Now, go to sakhacabs and run the dispatcher:

```
sudo service mongod start
cd /home/username/location/sakhacabs
python dispatcherapi.py
```



