import configparser
import os, sys,codecs

#dir_path = os.path.dirname(os.path.realpath(__file__))

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config = configparser.ConfigParser()

config.read_file(codecs.open(str(application_path)+'/config.ini', "r", "utf8"))

discordtoken = config['SETTINGS']['discordtoken'].strip()
prefix = config['SETTINGS']['prefix'].strip()