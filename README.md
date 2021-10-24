# plex-music-webhook
Basically creates a microserver that handles webhook from Plex
Plex webhook requires Plex subscription

## Installation
- Run 
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 sub/plex.py
```
- It should listen on the designated port and when webhook is triggered, it will write to now-playing.html file


## Instructions
- Go to config.json to set the port that you want this microserver to listen to (default to 44444)
- Ensure that you added the correct `http://[ip]:[port]` to https://app.plex.tv/desktop/#!/settings/webhooks
- Run `python3 sub/plex.py` to listen to the port
