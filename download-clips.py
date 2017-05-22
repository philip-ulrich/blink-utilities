#!/usr/bin/python3

'''
download-clips.py:
downloads blink clips and picks up where it left off

This should be ran as a cron job, but not too frequently. We do not want to
overwhelm the api servers. The cronjob should also be ran at the 59 minute mark
(or a couple minutes earlier) because of the "year" variable.

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

The last thing you need before running this, it to create a folder for each
camera. Note that spaces will be converted to '-'s. This will probably be
handled by the script eventually, but this is good enough for an initial
release.

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

import blinkpy, pickle, json
from datetime import datetime
from requests import get

def check_clips():
    global config
    year = str(datetime.now().year)
    last = config['last_download']
    download_list = []

    first = True
    blink = blinkpy.Blink(username=config['username'], 
                          password=config['password'])
    blink.setup_system()

    for event in blink.events:
        if event["type"] == "motion":
            if first == True and event['created_at'] != last:
                config['last_download'] = event['created_at']
                item={'url':'https://prod.immedia-semi.com'+event['video_url'],
                      'camera':event['camera_name'],'filename':
                      event['video_url'].rsplit('/', 1)[-1]}
                download_list.append(item)
                first = False
            else:
                if event['created_at'] != last:
                    if 'video_url' in event:
                        item={'url':'https://prod.immedia-semi.com'+
                              event['video_url'],'camera':event['camera_name'],
                              'filename':event['video_url'].rsplit('/', 1)[-1]}
                        download_list.append(item)
                else:
                    break

    headers = blink.get_auth_token()
    for item in download_list:
        filename = (item['camera'].replace(' ','-')+'/'+year+
                    item['filename'].split('_'+year,1)[-1].replace('_','-'))
        with open(filename, 'wb') as file:
            print("Downloading: {}".format(item['url']))
            response = get(item['url'], headers=headers)
            file.write(response.content)

with open('config.pickle', 'rb') as f:
    config = pickle.load(f)
# config['last_download'] = 0    # This is useful if you need to reset downloads
check_clips()
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)