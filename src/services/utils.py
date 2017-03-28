import os, json
from django.conf import settings
from boto.s3.connection import S3Connection, OrdinaryCallingFormat, VHostCallingFormat
from boto.s3.key import Key
from services.models import Option
import boto.s3
import datetime
import logging

logger = logging.getLogger(__name__)

def getFeed(userName='None'):
	feed = {}

	# options is used here as an example. you'll probably want to build your feed with different models
	feed['options'] = []

	for item in Option.objects.order_by('name'):
		option = {}
		option['id'] = item.id
		option['name'] = item.name
		option['value'] = item.value
		feed['options'].append(option)


	feed['meta'] = {
		'published': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'user': userName,
		'total': len(feed['options']),
	}

	return feed;

"""
Expects data to be json formatted (see getFeed above...)
"""
def uploadJSON(data, dest):
	# default to test bucket
	bucket_name = settings.AWS_BUCKET_TEST
	if dest == 'prod':
		bucket_name = settings.AWS_BUCKET_PROD

	# Write the combined feed to our json file
	jsonFile = '%s/json/feed.json' % settings.MEDIA_ROOT
	f = open(jsonFile, 'w')
	f.write(json.dumps(data, sort_keys=False, separators=(',', ':')))
	f.close()

	if settings.AWS_KEY:
		conn = boto.s3.connect_to_region(
			region_name = settings.AWS_BUCKET_REGION,
			aws_access_key_id = settings.AWS_KEY,
			aws_secret_access_key = settings.AWS_SECRET,
			calling_format = boto.s3.connection.OrdinaryCallingFormat())

		bucket = conn.get_bucket(bucket_name)

		k = Key(bucket)
		k.key = '/media/json/feed.json'
		k.set_contents_from_filename(jsonFile)
		bucket.set_acl('public-read', k.key)

		# also upload a time-stamped copy in case a rollback or history is needed
		# todo: make this disabled by default using a setting
		k.key = '/media/json/backup/%s.json' % data['meta']['published']
		k.set_contents_from_filename(jsonFile)
		bucket.set_acl('public-read', k.key)


