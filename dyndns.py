#!/usr/bin/python2.7
# Dynamic DNS for Linode
# By Tyler Rivera (tyler.rivera@gmail.com)
# inspiration from Jed Smith (jed@jedsmith.com)
# 
#
#

# Domain ID of your target domain
DOMAINID = ''
# Which record you want to change
RESOURCE = ''
# Your Linode API Key
API_KEY = ''
# Some address that will provide your public IP
IP_SERVICE = 'http://icanhazip.com'

API = 'https://api.linode.com/?api_key={0}&resultFormat=JSON'

try:
    from json import load
    from urllib import urlopen, urlretrieve, urlencode
except:
    print "Failure importing required modules"

def execute(action, parameters):

    uri = '{0}&action={1}'.format(API.format(API_KEY),action)
    if parameters and len(parameters) > 0:
        uri = "{0}&{1}".format(uri, urlencode(parameters))

    f, headers = urlretrieve(uri)
    
    json = load(open(f), encoding="utf-8")

    if len(json['ERRORARRAY']) > 0:
        err = json['ERRORARRAY'][0]
        raise Exception('Error {0}: {1}'.format(int(err['ERRORCODE']),
            err['ERRORMESSAGE']))

    return json

def ip():
    return urlopen(IP_SERVICE).read().strip()

def main():
    
    # Try and find the resource
    res = execute('domain.resource.list',{
        'ResourceID': RESOURCE,
        'DOMAINID': DOMAINID})['DATA'][0]
    public = ip()
    # If the IP is the same don't bother changing it
    if res['TARGET'] != public:
        old = res['TARGET']
        request = {
            'RESOURCEID': res['RESOURCEID'],
            'DOMAINID': res['DOMAINID'],
            'NAME': res['NAME'],
            'TYPE': res['TYPE'],
            'TARGET': public,
            'TTL_SEC': res['TTL_SEC']
        }
        print "Updating {0} -> {1}".format(old, public)
        execute('domain.resource.update', request)
    else:
        print "OK. No change required."
    
if __name__ == '__main__':
    main()