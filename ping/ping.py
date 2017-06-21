import pyping
import numpy as np
import redis
import os
from urllib2 import Request,urlopen

# global constants
EXTERNAL_ENDPOINTS = {'us-east1': '35.196.13.205', 'us-west1': '35.185.246.194', 'asia-east1':'35.185.137.79', 'asia-northeast1':'35.189.139.104', 'asia-southeast1':'35.187.232.105', 'europe-west1':'104.199.46.155', 'europe-west2': '35.189.70.26', 'us-central1':'130.211.145.80', 'us-east4': '35.186.181.15'}
INTERNAL_ENDPOINTS = {}
METADATA_ENDPOINT = 'http://metadata.google.internal/computeMetadata/v1/instance/zone'
r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)


# ping a region X times and region a latency average.
def ping_region(endpoint, times=10, timeout=2, psize=64):
  latency = []
  for _ in range(times):
    latency.append(pyping.do_one(endpoint, timeout, psize)*1000)
  return np.mean(latency)

# return the current region that the instance is
# located in.
def region():
  q = Request(METADATA_ENDPOINT)
  q.add_header('Metadata-Flavor', 'Google')
  a = urlopen(q).read()
  zone = a.rsplit('/', 1)[-1]
  region = zone.rsplit('-', 1)[0]
  return region

# write the results to redis as an hkey.
# <REGION_FROM> <REGION_TO> <LATENCY>
def write_results(results):
  region_from = region()
  for region_to,latency in results.items():
    r.hset(region_from,region_to,latency)

def main():
  latency_results = {}
  for k,v in EXTERNAL_ENDPOINTS.items():
    latency_results[k] = ping_region(v)
  write_results(latency_results)

main()
