#!/usr/bin/env python

import datetime
# import os for file system functions
import os
# import json
import json
# import regex
import re
# for date parsing
import time
# import flickrapi
# `easy_install flickrapi` or `pip install flickrapi`
import flickrapi

# main program
def fetch(api_key, api_secret):

  # create an unauthenticated flickrapi object
  flickr=flickrapi.FlickrAPI(api_key, api_secret)

  print "Open the following URL in your browser "
  print "This Url >>>> %s" % flickr.web_login_url(perms='read')

  print "When you're ready press ENTER",
  raw_input()

  print "Copy and paste the URL (from theopenphotoproject.org) here: ",
  frob_url = raw_input()

  print "\nThanks!"

  print "Parsing URL for the token...",
  match = re.search('frob=([^&]+)', frob_url)
  frob = match.group(1)
  token = flickr.get_token(frob)
  print "OK"

  # create an authenticated flickrapi object
  flickr = flickrapi.FlickrAPI(api_key, api_secret, token=token)

  # now we get the authenticated user's id
  print "Fetching user id...",
  user_resp = flickr.urls_getUserProfile()
  user_fields = user_resp.findall('user')[0]
  user_id = user_fields.get('nsid')
  print "OK"
  

# print "Enter your token: ",
# token = raw_input()
  per_page = 100

  (token, frob) = flickr.get_token_part_one('read')
  flickr.get_token_part_two((token, frob))

  # we'll paginate through the results
  # start at `page` and get `per_page` results at a time
  page=1

  # store everything in a list or array or whatever python calls this
  photos_out=[]

  # while True loop till we get no photos back
  while True:
    # call the photos.search API
    # http://www.flickr.com/services/api/flickr.photos.search.html
    print "Fetching page %d..." % page,
    photos_resp = flickr.people_getPhotos(user_id=user_id, per_page=per_page, page=page, extras='original_format,tags,geo,url_o,url_b,url_c,url_z,date_upload,date_taken,license,description')
    print "OK"

    # increment the page number before we forget so we don't endlessly loop
    page = page+1;

    # grab the first and only 'photos' node
    photo_list = photos_resp.findall('photos')[0]

    # if the list of photos is empty we must have reached the end of this user's library and break out of the while True
    if len(photo_list) == 0:
      break;

    # else we loop through the photos
    for photo in photo_list:
      # get all the data we can
      p = {}
      p['id'] = photo.get('id')
      p['permission'] = bool(int(photo.get('ispublic')))
      p['title'] = photo.get('title')
      p['license'] = getLicense(photo.get('license'))
      description = photo.findall('description')[0].text
      if description is not None:
        p['description'] = description

      if photo.get('latitude') != '0':
        p['latitude'] = float(photo.get('latitude'))

      if photo.get('longitude') != '0':
        p['longitude'] = float(photo.get('longitude'))

      if len(photo.get('tags')) > 0:
        p['tags'] = photo.get('tags').split(' ')
      else:
        p['tags'] = []
      if photo.get('place_id') is not None:
        p['tags'].append("flickr:place_id=%s" % photo.get('place_id'))

      if photo.get('woe_id') is not None:
        p['tags'].append("geo:woe_id=%s" % photo.get('woe_id'))

      p['tags'] = ",".join(p['tags'])
      p['dateUploaded'] = int(photo.get('dateupload'))
      p['dateTaken'] = int(time.mktime(time.strptime(photo.get('datetaken'), '%Y-%m-%d %H:%M:%S')))

      # Attention : this is returned only for Pro accounts, it seems
      if photo.get('url_o') is not None:
        p['photo'] = photo.get('url_o')
      elif photo.get('url_b') is not None:
        p['photo'] = photo.get('url_b')
      elif photo.get('url_c') is not None:
        p['photo'] = photo.get('url_c')
      elif photo.get('url_z') is not None:
        p['photo'] = photo.get('url_z')

      t = datetime.datetime.fromtimestamp(float(p['dateUploaded']))
      filename = '%s-%s' % (t.strftime('%Y%m%dT%H%M%S'), p['id'])

      print "  * Storing photo %s to fetched/%s.json" % (p['id'], filename),
      f = open("fetched/%s.json" % filename, 'w')
      f.write(json.dumps(p))
      f.close()
      print "OK"

# create a directory only if it doesn't already exist
def createDirectorySafe( name ):
  if not os.path.exists(name):
    os.makedirs(name)

# construct the url for the original photo
# currently this requires a pro account
def constructUrl( photo ):
  return "http://farm%s.staticflickr.com/%s/%s_%s_o.%s" % (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('originalsecret'), photo.get('originalformat'))

# map Flickr licenses to short names
def getLicense( num ):
  licenses = {}
  licenses['0'] = ''
  licenses['4'] = 'CC BY'
  licenses['5'] = 'CC BY-SA'
  licenses['6'] = 'CC BY-ND'
  licenses['2'] = 'CC BY-NC'
  licenses['1'] = 'CC BY-NC-SA'
  licenses['3'] = 'CC BY-NC-ND'

  if licenses[num] is None:
    return licenses[0]
  else:
    return licenses[num]


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Backup your Flickr photos')
  parser.add_argument('--api-key', required=True, help='Flickr API key')
  parser.add_argument('--api-secret', required=True, help='Flickr API secret')

  config = parser.parse_args()

  # check if a fetched directory exist else create it
  createDirectorySafe('fetched')
  fetch(config.api_key, config.api_secret)
