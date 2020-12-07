#!/usr/bin/env python3

import sys

sys.path.insert(0, './ptpy')

from ptpy import PTPy

camera = PTPy(knowledge=False)

print(camera.get_device_info());
 
with camera.session():
    camera.get_config_info()
    with open("config.dat", "wb") as file:
        file.write(camera.get_config_backup().Data)
