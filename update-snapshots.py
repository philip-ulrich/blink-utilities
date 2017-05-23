#!/usr/bin/python3

'''
update-snapshots.py:
updates the snapshots shown on your cameras

This should be ran as a cron job, but not too frequently. We do not want to
overwhelm the api servers or drain your batteries too much. Additionally, there
are time constraints added for times that you don't want updates (like sleeping).
You can remove this by taking out the line:

    if datetime.now().hour < 20 or datetime.now().hour > 8:

and de-indenting:

    update_snapshots()

Or modify it to change your down time. 

Please see the requirements.txt for external modules needed.

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

## 1.0.1 - 2017-05-23
### Added
- Time parameters for updating a snapshot (I don't need updates while sleeping)
- Print outputs for success or failure
### Changed
- Put try/except around things that could ocassionally fail and break the cycle
- Changed sleep to 10 seconds. 5 seconds was causing system is busy

## 1.0.0 - 2017-05-21
### Added
- Initial release
'''
__author__     = "Philip Ulrich"
__copyright__  = "Copyright 2017, Philip Ulrich"
__credits__    = "Philip Ulrich"
__license__    = "MIT"
__version__    = "1.0.1"
__maintainer__ = "Philip Ulrich"
__email__      = "philip@exec.tech"
__status__     = "Production"

import blinkpy, pickle, time
from datetime import datetime

def update_snapshots():
    global config

    blink = blinkpy.Blink(username=config['username'], 
                          password=config['password'])
    try:
        blink.setup_system()

        for camera in blink.cameras:
            try:
                blink.cameras[camera].snap_picture()
            except Exception as e:
                print(e)
            else:
                print("{} snapshot has been updated.".format(camera))
            time.sleep(10)
    except Exception as e:
        print(e)

with open('config.pickle', 'rb') as f:
    config = pickle.load(f)
if datetime.now().hour < 20 or datetime.now().hour > 8:
    update_snapshots()
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)


