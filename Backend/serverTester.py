import requests
import json
import urllib2
import base64
def makeUser(username, password, name):
    return {'username':username, 'password':password, 'name':name}
if __name__ ==  '__main__':
    # user1 = makeUser('davide', 'password', 'davidyang')
    # r = requests.post('http://127.0.0.1:3030/users/', data=json.dumps(user1))
    # print r.text

    r = urllib2.urlopen("http://127.0.0.1:3030/data/?id=-Jzd0-9MrcDnXBiJOS0a").read()   
    print r

    # r = urllib2.urlopen("http://127.0.0.1:3030/users/?username=davide").read()
    # print r

    # f = open('test2.png', 'rb')
    # undecode = base64.b64encode(f.read())
    # payload = {'username':"davide", 'rating':1, 'lat':15, 'lon':25, 'serializedImage':undecode}
    # r = requests.post('http://127.0.0.1:3030/data/', data=json.dumps(payload))

    # r = urllib2.urlopen("http://127.0.0.1:3030/data/?quant=10&qType=1&username=davide&lat=0&lon=0").read()
    # l = json.loads(r)
    # for i in l:
    #     print i['lat'],i['lon'],i['username']
    #print r
