import redis
import json
import time
import googleapiclient.discovery
import http
from StringIO import StringIO


# JSON structure that is created
# {
#    "datetime": "<datetime>",
#    "latencies": {
#       "<region_from>": {
#          "<region_to>": "<latency>"
#       }
#    }
# }

REGIONS = ['us-east1', 'us-west1', 'asia-east-1', 'asia-northeast1', 'asia-southest1', 'europe-west1', 'europe-west2', 'us-central1', 'us-east4']
r = redis.StrictRedis(host='redis-10800.c1.us-east1-2.gce.cloud.redislabs.com', port=10800, db=0)

def main():
  data = {}
  data['latencies'] = {}
  for region in REGIONS:
    latencies = r.hgetall(region)
    data['latencies'][region] = latencies

  data['datetime'] = time.strftime("%Y-%m-%d %H:%M")
  upload_to_google_storage(data)

def upload_to_google_storage(data):
  service = googleapiclient.discovery.build('storage', 'v1')
  bucket_name = 'gcp-latency'
  media = googleapiclient.http.MediaIoBaseUpload(StringIO(json.dumps(data)), mimetype='plain/text')

  req = service.objects().insert(
    bucket=bucket_name,
    body={"cacheControl": "public,max-age=31536000"},
    media_body=media,
    predefinedAcl='publicRead',
    name='latency_results',
  )
  resp = req.execute()

main()
