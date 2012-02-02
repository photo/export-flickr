# import os for file system functions
import os
# import flickrapi
# pip install flickrapi
import flickrapi
# import json
import json

# main program
def main():
  # get api key, secret and token from the user
  print "Enter your api key: ",
  api_key = raw_input()
  print "Enter your api secret: ",
  api_secret = raw_input()
  print "Enter your token: ",
  token = raw_input()
  print "How many photos per request? (100 if you aren't sure): ",
  per_page = raw_input()

  # create a flickrapi object
  flickr=flickrapi.FlickrAPI(api_key, api_secret, token=token)

  # we'll paginate through the results
  # start at `page` and get `per_page` results at a time
  page=1

  # store everything in a list or array or whatever python calls this
  photos_out=[]

  # while True loop till we get no photos back
  while True:
    # call the photos.search API
    # http://www.flickr.com/services/api/flickr.photos.search.html
    photos=flickr.photos_search(user_id='63789665@N05', per_page=per_page, page=page, extras='original_format')

    # increment the page number before we forget so we don't endlessly loop
    page=page+1;

    # grab the first and only 'photos' node
    photo_list=photos.findall('photos')[0]

    # if the list of photos is empty we must have reached the end of this user's library and break out of the while True
    if len(photo_list) == 0:
      break;

    # else we loop through the photos
    for photo in photo_list:
      # get all the data we can
      photo_id=photo.get('id')
      photo_permission=photo.get('ispublic')
      photo_title=photo.get('title')
      photo_has_geo=photo.get('has_geo')

      f = open("fetched/%s.json" % photo_id, 'w')
      f.write("%r" % {'id':photo_id,'title':photo_title,'url':constructUrl(photo)})
      f.close()

      print "photo %s stored to fetched/%s.json" % (photo_id, photo_id)

# create a directory only if it doesn't already exist
def createDirectorySafe( name ):
  if not os.path.exists(name):
    os.makedirs(name)

# construct the url for the original photo
# currently this requires a pro account
def constructUrl( photo ):
  return "http://farm%s.staticflickr.com/%s/%s_%s_o.%s" % (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('originalsecret'), photo.get('originalformat'))



# check if a fetched directory exists
createDirectorySafe('fetched')
createDirectorySafe('processed')
createDirectorySafe('errored')
main()
