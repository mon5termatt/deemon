#!/usr/bin/env python3
from deemon.utils import startup

from deemon.core.common import map_track as new_map_track

import deezer.utils
deezer.utils.map_track = new_map_track

__version__ = '2.22'
__dbversion__ = '3.7'

appdata = startup.get_appdata_dir()
startup.init_appdata_dir(appdata)
