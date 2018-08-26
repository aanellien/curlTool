import requests
import enum
import base64
import time

class Scope(enum.Enum):
    data_read= 'data:read'
    create_bucket = 'bucket:create'
    write_data = 'data:write'
    read_write_data='data:read data:write'
    read_viewable= 'viewables:read'

def getToken(scope):
    url = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
    headers= {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'client_id':'l7SwtiVH1IoGTAKRN7CXjuHT9d3FQZam',
        'client_secret': 'HGF4cEGo1vxZ7WRB',
        'grant_type': 'client_credentials',
        'scope': scope
     }

    r = requests.post(url,headers=headers,data=payload)
    return r.json()['access_token']



def createBucket(token,bucket_name):
    url= 'https://developer.api.autodesk.com/oss/v2/buckets'
    headers= {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer '+token),
    }
    payload = {
        'bucketKey': bucket_name,
        'policyKey': 'transient'
    }
    r = requests.post(url,headers=headers,json=payload)
    return r.status_code

def uploadFile(token, bucketName, fileName , file):
    url = 'https://developer.api.autodesk.com/oss/v2/buckets/{0}/objects/{1}'.format(bucketName,fileName)
    headers= {
        'Authorization': ('Bearer '+token),
    }
    #files = {'file': open(filePath, 'rb')}
    r = requests.put(url,headers=headers,data=file)
    return r.json()['objectId']



def convertFile(token,urn):
    url= 'https://developer.api.autodesk.com/modelderivative/v2/designdata/job'

    headers= {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer '+token),
    }

    data = {
        'input': {'urn': urn},
        'output': {
            'destination': {'region': 'us'},
            'formats': [{
                'type': 'svf',
                'views': ['2d', '3d']
            }]
        }
    }
    r= requests.post(url,headers=headers,json=data)
    return r.status_code


def checkConversionStatus(token,urn):
    url = 'https://developer.api.autodesk.com/modelderivative/v2/designdata/{0}/manifest'.format(urn)
    headers= {
        'Authorization': ('Bearer '+token),
        'Cache-Control': 'no-cache'
    }
    r=requests.get(url,headers=headers)
    print r.status_code
    return r.json()['progress']

def waitUntilConvert(token,urn):
    status=checkConversionStatus(token,urn)
    print status
    while(status!= 'complete'):
        status=checkConversionStatus(token,urn)
        print status
        time.sleep(1)


def fullWorkFlow(bucket,fileName,file):
    print createBucket(getToken(Scope.create_bucket),bucket)
    print 'bucket created'
    urn=  uploadFile(getToken(Scope.write_data), bucket, fileName,file )
    urn = base64.b64encode(urn)
    print 'file uploaded'
    print convertFile(getToken(Scope.read_write_data),urn)
    print 'file conversion started'
    waitUntilConvert(getToken(Scope.data_read),urn)
    return urn

if( __name__ == '__main__ '):
    bucket = 'aanellien_bucket_7'
    print createBucket(getToken(Scope.create_bucket),bucket)
    print 'bucket created'
    urn=  uploadFile(getToken(Scope.write_data), bucket, 'dragon.fbx','Dragon 2.5_fbx.fbx' )
    urn = base64.b64encode(urn)
    print 'file uploaded'
    print convertFile(getToken(Scope.read_write_data),urn)
    print 'file conversion started'
    waitUntilConvert(getToken(Scope.data_read),urn)
    print getToken(Scope.read_viewable)
    print urn
