import os
import json


CONFIG_FILE = './config.json'
print(CONFIG_FILE)

try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        PROD = config['PROD']
        print(config['PROD'])
        print(PROD)
        if PROD=="True":
            from .prod import *
            print("try prod")
        else:
            print(" try dev")
            from .dev import *


except KeyError:
    print("except dev")
    from .dev import *
    print("apres dev")
