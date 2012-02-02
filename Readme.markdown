Open Photo API / Export tool for Flickr
=======================
#### OpenPhoto, a photo service for the masses

----------------------------------------

## How to use

This script fetches all of your photos from Flickr and stores them into text files which can then be easily imported to OpenPhoto.

Before you get started you'll need a Flickr API key.

* http://www.flickr.com/services/apps/create/

You'll need an authentication token to actually run this script (not yet implemented).

    python fetch.py

The script will ask for your API key, secret, token and the number of photos per request. It should look something like this

      Enter your api key:  ********************************
      Enter your api secret:  ****************
      Enter your token:  **********************************
      How many photos per request? (100 if you aren't sure):  100
      photo 6109695003 stored to fetched/6109695003.json
      photo 6109694841 stored to fetched/6109694841.json
      photo 6109694637 stored to fetched/6109694637.json
      photo 6110240318 stored to fetched/6110240318.json
      photo 6110240222 stored to fetched/6110240222.json
      photo 6065502023 stored to fetched/6065502023.json

## YAY
