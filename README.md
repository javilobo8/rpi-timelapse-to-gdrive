# RPi Timelapse to GDrive
Take photos with a Raspberry Pi and upload to GDrive

## Installation

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib PyDrive
```

Fill `settings.yaml` with your clientid and your secret retreived from here [https://developers.google.com/drive/api/v3/quickstart/python](https://developers.google.com/drive/api/v3/quickstart/python)

Run creds.py to generate credentials.json
```bash
python creds.py
```

## Usage

Execute script
```bash
python run.py
```

You can create a crontask with `crontab -e` and insert the following line to run the script every 10 minutes

```
*/10 * * * * cd /path/to/repo && /usr/bin/python run.py
```
