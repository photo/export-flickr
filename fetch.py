# import os for file system functions
import os
# import flickrapi
# pip install flickrapi
import flickrapi
# import json
import json
# import regex
import re

def auth(frob, perms):
    print 'Please give us permission %s' % perms

# main program
def main():

  # get api key, secret and token from the user
  print "Enter your api key: ",
  api_key = raw_input()
  print "Enter your api secret: ",
  api_secret = raw_input()

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
    photos_resp = flickr.people_getPhotos(user_id=user_id, per_page=per_page, page=page, extras='original_format')
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
      photo_id = photo.get('id')
      photo_permission = photo.get('ispublic')
      photo_title = photo.get('title')
      photo_has_geo = photo.get('has_geo')

      print "  * Storing photo %s to fetched/%s.json..." % (photo_id, photo_id),
      f = open("fetched/%s.json" % photo_id, 'w')
      f.write("%r" % {'id':photo_id,'title':photo_title,'url':constructUrl(photo)})
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



# check if a fetched, processed and errored directories exist
createDirectorySafe('fetched')
createDirectorySafe('processed')
createDirectorySafe('errored')
main()
