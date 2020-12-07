#!/usr/bin/env python3

import sys

sys.path.insert(0, './ptpy')

from ptpy import PTPy

camera = PTPy(knowledge=False)

print(camera.get_device_info());
 
with camera.session():
    object_info = camera.get_config_info().Data
    camera.send_object_info(object_info)

    with open("config.dat", "rb") as file:
        print(camera.send_object(file.read()))
