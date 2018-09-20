import sys,os,telegram
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



User.set_db(db)
LocationUpdate.set_db(db)
DutySlip.set_db(db)
#a=telegram.ext.MessageHandler(telegram.ext.Filters.all,messagehandler)
#driversakhabot.updater.dispatcher.add_handler(a)
'''
dp = driversakhabot.updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],

        PHOTO: [MessageHandler(Filters.photo, photo),
                CommandHandler('skip', skip_photo)],

        LOCATION: [MessageHandler(Filters.location, location),
                   CommandHandler('skip', skip_location)],

        BIO: [MessageHandler(Filters.text, bio)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

dp.add_handler(conv_handler)
    # log all errors
dp.add_error_handler(error)
'''
#driversakhabotkarta=sakhacabsxpal.start_pykka_karta()
#driversakhabotkarta.tell({'msg':'run','func':xetrapal.telegramkarmas.poll,'args':[driversakhabot,"/home/arjun/sakhacabs/driversakhastop" ],'kwargs':{}})
