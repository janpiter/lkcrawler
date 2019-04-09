from ConfigParser import ConfigParser
import os


def load(config_file="config.ini"):
    config_path = "{}/{}".format(os.getcwd(), config_file)
    config = ConfigParser()
    config.read(config_path)
    return config
