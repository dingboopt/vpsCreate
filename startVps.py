import json
import requests
import time
import subprocess
import sys

print "arg count is "
print len(sys.argv)

if (sys.argv[1] == '-h'):
    print "usage: username password bandwith"

username = sys.argv[1]
password = sys.argv[2]
bandwith = sys.argv[3]
if bandwith > '5' or bandwith <'1':
    print 'bandwith >5 set to 1'
    bandwith = 1

print "bandwith is:"
print bandwith

if (len(sys.argv)>4) :
    ipToBind= sys.argv[4]
else:
    ipToBind = None 

url = 'https://iam.ap-southeast-1.myhwclouds.com/v3/auth/tokens'
headers = {'Content-type': 'application/json'}
data = {u'auth': {u'scope': {u'project': {u'name': u'ap-southeast-1'}},u'identity': {u'password': {u'user': {u'domain': {u'name': username}, u'password': password, u'name': username}}, u'methods': [u'password']}}}

resp = requests.post(url=url, data=json.dumps(data), headers=headers )
#data = resp.json() 
print resp.headers
headers = resp.headers
token = headers['x-subject-token']
print token

headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
if ipToBind is not None:
    url = 'https://vpc.ap-southeast-1.myhuaweicloud.com/v1/d915e1d6c7c845e88f3d4d099e671bee/publicips'
    resp = requests.get(url=url, headers=headers )
    print resp.text
    publicips = json.loads(resp.text)['publicips']
    publicipId = None
    for i in range(0, len(publicips)):
        if publicips[i]['public_ip_address'] == ipToBind:
            publicipId = publicips[i]['id'] 
            break;

url = 'https://ecs.ap-southeast-1.myhuaweicloud.com/v1.1/d915e1d6c7c845e88f3d4d099e671bee/cloudservers'
data = {u'server': {u'vpcid': u'abf2d62b-767c-4951-9fca-bbfb42ff8e02', u'name': u'whatthefuck1', u'imageRef': u'cbe0df31-1150-488a-a9b2-612c745e1be0', u'availability_zone': u'ap-southeast-1a', u'nics': [{u'subnet_id': u'3304ec10-204a-4c1a-b49c-bc385bb4c8db'}], u'flavorRef': u's3.small.1', u'adminPass': u'Huawei@123', u'publicip': {u'eip': {u'bandwidth': {u'sharetype': u'PER', u'size': bandwith}, u'iptype': u'5_bgp'}}, u'security_groups': [{u'id': u'9401486d-5a37-4e20-95f1-03ed6f43ca92'}], u'root_volume': {u'volumetype': u'SATA'}}}

if publicipId is not None:
    data['publicip'] = {'id': publicipId}
resp = requests.post(url=url, data=json.dumps(data), headers=headers )
print resp


if publicipId is None:
    url = 'https://vpc.ap-southeast-1.myhuaweicloud.com/v1/d915e1d6c7c845e88f3d4d099e671bee/publicips'
    
    for i in range(0,20):
        try:
            resp = requests.get(url=url, headers=headers )
            publicIp = json.loads(resp.text)['publicips'][0]['public_ip_address']
            break
        except Exception as e:
            print e
            time.sleep(2)
else:
    publicIp = ipToBind

print publicIp

for i in range(0,20):
    retcode = subprocess.call(["sshpass", "-p", "Huawei@123", "ssh", "-oStrictHostKeyChecking=no", "root@"+publicIp, "pwd"])
    if retcode == 0:
        break;
    else:
        time.sleep(2)
print "begin to upload"
retcode = subprocess.call(["sshpass", "-p", "Huawei@123", "scp", "-oStrictHostKeyChecking=no", "./vpn.sh", "root@"+publicIp+":/root/"])
print retcode


print "begin to execute"
retcode = subprocess.call(["sshpass", "-p", "Huawei@123", "ssh", "-oStrictHostKeyChecking=no", "root@"+publicIp, "sh", "vpn.sh"])

print retcode


retcode = subprocess.call(["ssh-keygen", "-f", "/root/.ssh/known_hosts", "-R" ,publicIp])

print retcode

retcode = subprocess.call(["rm", "/data/data/com.termux/files/home/.ssh/known_hosts"])

print retcode

print publicIp
