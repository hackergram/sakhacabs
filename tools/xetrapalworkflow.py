import sys
sys.path.append("/opt/xetrapal")
import xetrapal
sys.path.append("/opt/mojomailman/mojomail")
from mojomailGMail import *
sakhacabsxpal=xetrapal.Xetrapal(configfile="/home/arjun/sakhacabs/sakhacabsxpal.conf")
sakhamailer=sakhacabsxpal.get_mojomail()
