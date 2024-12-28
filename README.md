Inspired by [How I Built an NFC Movie Library for my Kids](https://simplyexplained.com/blog/how-i-built-an-nfc-movie-library-for-my-kids/)([HN](https://news.ycombinator.com/item?id=41479141)) with some modifications to use Chromecast and Jellyfin instead of Plex and Apple TV.


# Install esphome

Create a virutal env and activate it. Then install the esphome requirements.

```
python3 -m venv .venv --prompt homeassistant-nfc-chromecast
source .venv/bin/activate
pip install -r requirements.txt
```

# Flash esphome

Copy `secrets-example.yaml` to `secrets.yaml` and set the WiFi password and API password. Then connect the ESP32 microcontroller to USB and run:

```
esphome run configuration.yaml
```

# Configure Home Assistant

Create an Automation for Home Assistant after editing `automation.yaml` to use the shows from your Jellyfin library. 

To get the Jellyfin ids open the Jellyfin web interface and extract it from the URL. For example this show will have the ID `c972a911b238ff4e4e864431a559b1c6`:

```
http://jellyfin.example.com:8096/web/#/details?id=c972a911b238ff4e4e864431a559b1c6
```

To get the tag ID use Home Assistant -> Developer Tools -> Events and listen to the `tag_scanned` event. Scan a tag and it will dump the tag id like 8D-B5-18-03.

# Getting a List of Jellyfin IDs

To have a tag select a random episode from a playlist you need to get all of the show's IDs. This is tedious to do manually so I wrote a script.

The most annoying bit is getting the Library ID. The only way I can figure out how to find it is via a broswer inspection of the Library and seeing the 'data-id' field for the Library card. Please let me know if there is a better way.

```
python jellyfin-dump-ids.py \
  --base-url http://jellyfin.example.com:8096 \ 
  --library-id FIND_VIA_DEV_CONSOLE_ON_LIBRARY_DASHBOARD \ 
  --api-key GENERATE_IN_JELLYFIN_DASHBOARD \ 
  --show-name "Game Novel"
```
