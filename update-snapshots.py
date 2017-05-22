#!/usr/bin/python3

'''
update-snapshots.py:
updates the snapshots shown on your cameras

This should be ran as a cron job, but not too frequently. We do not want to
overwhelm the api servers or drain your batteries too much.

Please see the requirements.txt for modules needed.

As with the other utilities you will have no pickle intitially. I would
you use the same config pickle for all the utilities. You can use the code below
to generate this:

###############################################################################

data = {
    'last_download': '0',
    'username': '',
    'password': ''
}

with open('config.pickle', 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

###############################################################################

## 1.0.0 - 2017-05-21
### Added
- Initial release
'''
__author__     = "Philip Ulrich"
__copyright__  = "Copyright 2017, Philip Ulrich"
__credits__    = "Philip Ulrich"
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "Philip Ulrich"
__email__      = "philip@exec.tech"
__status__     = "Production"

import blinkpy, pickle, time

def update_snapshots():
    global config

    blink = blinkpy.Blink(username=config['username'], 
                          password=config['password'])
    blink.setup_system()

    for camera in blink.cameras:
        blink.cameras[camera].snap_picture()
        time.sleep(5)

with open('config.pickle', 'rb') as f:
    config = pickle.load(f)
update_snapshots()
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)
