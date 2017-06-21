import redis
import json
import time
import googleapiclient.discovery
import http
import os
import pandas as pd
import numpy as np
from StringIO import StringIO


REGIONS = ['us-east1', 'us-west1', 'asia-east1', 'asia-northeast1', 'asia-southeast1', 'europe-west1', 'europe-west2', 'us-central1', 'us-east4']
r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

def main():
  my_df = []
  for source_region in REGIONS:
    latencies = r.hgetall(source_region)

    d = {}
    d['region'] = source_region

    for dest_region, latency in latencies.iteritems():
      d[dest_region] = latency
      my_df.append(d)

  my_df = pd.DataFrame(my_df)
  my_df = my_df.convert_objects(convert_numeric=True)
  my_df = my_df.round(2)
  my_df.drop_duplicates(inplace=True)
  my_df = my_df.set_index('region')
  my_df.sort_index(axis=1, inplace=True)

  # fill diagonal with 0s
  my_df = my_df.reindex(columns=list(my_df.index) + list(my_df.columns.difference(my_df.index)))
  np.fill_diagonal(my_df.values,0)

  # convert to string
  my_df.to_csv('data.csv')
  s = StringIO()
  my_df.to_csv(s)

  upload_to_google_storage(s)

def upload_to_google_storage(data):
  service = googleapiclient.discovery.build('storage', 'v1')
  bucket_name = 'gcp-latency'
  media = googleapiclient.http.MediaIoBaseUpload(data, mimetype='plain/text')

  req = service.objects().insert(
    bucket=bucket_name,
    body={"cacheControl": "public,max-age=31536000"},
    media_body=media,
    predefinedAcl='publicRead',
    name='latencies.csv',
  )
  resp = req.execute()

main()
