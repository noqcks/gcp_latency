import googleapiclient.discovery

compute = googleapiclient.discovery.build('compute', 'v1')

compute.instances().start(project='noqcks', instance='us-east-1-ping', zone='us-east1-c').execute()
compute.instances().start(project='noqcks', instance='asia-east1-ping', zone='asia-east1-a').execute()
compute.instances().start(project='noqcks', instance='asia-northeast1-ping', zone='asia-northeast1-a').execute()
compute.instances().start(project='noqcks', instance='asia-southeast1-ping', zone='asia-southeast1-a').execute()
compute.instances().start(project='noqcks', instance='europe-west1-ping', zone='europe-west1-d').execute()
compute.instances().start(project='noqcks', instance='europe-west2-ping', zone='europe-west2-b').execute()
compute.instances().start(project='noqcks', instance='us-central1-ping', zone='us-central1-c').execute()
compute.instances().start(project='noqcks', instance='us-east4-a', zone='us-east4-a').execute()
compute.instances().start(project='noqcks', instance='us-west-1', zone='us-west1-b').execute()

print "started instances"
