import sys
sys.path.append("/opt/xetrapal")
import xetrapal
sys.path.append("/opt/mojomailman/mojomail")
from mojomailGMail import *
sys.path.append("/opt/sakhacabs/lib")
from sakhacabsfunctions import *
sakhacabsxpal=xetrapal.Xetrapal(configfile="/home/arjun/sakhacabs/sakhacabsxpal.conf")
sakhamailer=sakhacabsxpal.get_mojogmail()
driverbotconfig=xetrapal.karma.load_config(configfile="/home/arjun/sakhacabs/driversakhabot.conf")
sakhahelperconfig=xetrapal.karma.load_config(configfile="/home/arjun/sakhacabs/sakhahelper.conf")

driversakhabot=xetrapal.telegramastras.XetrapalTelegramBot(config=driverbotconfig,logger=sakhacabsxpal.logger)
sakhahelper=xetrapal.telegramastras.XetrapalTelegramBot(config=sakhahelperconfig,logger=sakhacabsxpal.logger)

server=Server()
db=server['sakhacabs']

User.set_db(db)