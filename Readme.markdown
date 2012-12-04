Open Photo API / Export tool for Flickr
=======================
#### OpenPhoto, a photo service for the masses

----------------------------------------

<a name="overview"></a>
### Overview

This script fetches all of your photos from Flickr and stores them into text files which can then be easily imported to OpenPhoto.

<a name="setup"></a>
### Setting up an API key

Before you get started you'll need a Flickr API key.

1. Go to http://www.flickr.com/services/apps/create/apply/
1. Apply for a non-commercial key
1. Provide a name and description (this can be anything)
1. Take note of your key and secret, you'll need them soon
1. Click Edit auth flow for this app
1. Put anything in for the callback URL, http://theopenphotoproject.org works
1. Save changes

<a name="dependencies"></a>
### Getting dependencies

The only dependency you need the `flickrapi` module.

    sudo easy_install flickrapi
    # you may also use pip to install it
    # sudo pip install flickrapi

If you're using Ubuntu or Debian, their package should also work:

    sudo aptitude install python-flickrapi

<a name="download"></a>
### Downloading the script

#### Using git

    git clone git://github.com/photo/export-flickr.git

#### Using wget

    mkdir export-flickr
    wget -O export-flickr/fetch.py https://raw.github.com/photo/export-flickr/master/fetch.py --no-check-certificate

#### Using file->save

Click the link below and save the file into a directory named `export-flickr`.

https://raw.github.com/photo/export-flickr/master/fetch.py

<a name="running"></a>
### Running the script

Start a terminal and enter the following.

    cd export-flickr
    python fetch.py --api-key=******************************** --api-secret=****************

For api-key and api-secret, enter what Flickr returned you in step 4 of above.

Next you'll be given a URL which you need to copy and paste into a browser. If you're not logged into Flickr you'll have to sign in. Once logged in you need to approve the application access to your account.

_NOTE:_ This script ONLY asks for read permissions. If it's asking for write permissions throw your computer in the trash.

    Open the following URL in your browser 
    This Url >>>> http://api.flickr.com/services/auth/?perms=read&api_sig=********************************&api_key=********************************

After this you'll be redirected to the URL you specified as your callback. Copy and paste the entire URL into the terminal.

    When you're ready press ENTER 
    Copy and paste the URL (from theopenphotoproject.org) here:  http://theopenphotoproject.org/?frob=*******************************************

    Thanks!

Now the script gets to work downloading the information for your photos. It doesn't download the actual photos so it should be relatively fast.

    Parsing URL for the token... OK
    Fetching user id... OK
    Fetching page 1... OK
      * Storing photo 6109695003 to fetched/6109695003.json... OK
      * Storing photo 6109694841 to fetched/6109694841.json... OK
      * Storing photo 6109694637 to fetched/6109694637.json... OK
      * Storing photo 6110240318 to fetched/6110240318.json... OK
      * Storing photo 6110240222 to fetched/6110240222.json... OK
      * Storing photo 6065502023 to fetched/6065502023.json... OK
    Fetching page 2... OK

### YAY

Now you've got a bunch of text files. These can be fed into our [import tool](http://github.com/photo/import) to transfer all of your photos into your OpenPhoto account.

Don't worry, we'll have a nice web based GUI for all of this soon :).

<a name="knownissues"></a>
### Known issues

1. Fetches URL of original photos, which only works for Flickr pro accounts.
1. Flickr allows multiple licenses but OpenPhoto does not.
1. Flickr has machine tags, do we implement something similar?
   * Proposal is to store them even if we don't do anything *special* with them
1. Flickr has a place_id
   * Proposal is to store it as a tag `flickr:place_id=xxxxxxx`
1. Flickr has a woe_id (http://developer.yahoo.com/geo/geoplanet/guide/concepts.html)
   * Proposal is to store it as a tag `geo:woe_id=xxxxxxx`
   * Since it's not Flickr specific (maybe Yahoo! specific) store it as a geo attribute
1. How to deal with contacts and groups?
   * Proposal is to auto create two groups (friends and family) and add photos to the given group for permissions. The user can then add people to the group since we won't import the actual contacts. This way if a photo is to be shared with family, it still is once they add family members to their group.

