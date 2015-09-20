import requests
import json
import urllib
import urllib2
import base64
def makeUser(username, password, name):
    return {'username':username, 'password':password, 'name':name}
if __name__ ==  '__main__':
    """
    users = [makeUser('david', 'password', 'david'), makeUser('sylvia', 'password', 'sylvia'), makeUser('margaret', 'password', 'sylvia')]
    for user in users:
        requests.post('http://127.0.0.1:8000/users/', data=json.dumps(user))
        print user

    f = open('examples', 'r')
    for i in range(10):
        username = f.readline().rstrip()
        name = f.readline().rstrip()
        #print name
        url = f.readline().rstrip()
        urllib.urlretrieve(url, "temp.jpg")
        print url
        g = open("temp.jpg", 'rb')
        undecode = base64.b64encode(g.read())
        gps = f.readline().split()
        ##print gps
        #gps = gps.split()
        # print gps[0]
        # print gps[1]
        lat = float(gps[0])
        lon = float(gps[1])
        rating = int(f.readline())
        requests.post('http://127.0.0.1:8000/data/', data=json.dumps({'username':username, 'name':name, 'lat':lat, 'lon':lon, 'rating':rating, 'serializedImage': undecode}))
        """
    # user1 = makeUser('davide', 'password', 'davidyang')
    # r = requests.post('http://127.0.0.1:3030/users/', data=json.dumps(user1))
    # print r.text

    # r = urllib2.urlopen("http://127.0.0.1:3030/data/?id=-Jzd0-9MrcDnXBiJOS0a").read()
    # print r

    # r = urllib2.urlopen("http://127.0.0.1:3030/users/?username=davide").read()
    # print r

    # f = open('test2.png', 'rb')
    # undecode = base64.b64encode(f.read())
    # payload = {'name':'name','username':"davide", 'rating':1, 'lat':15, 'lon':25, 'serializedImage':undecode}
    # r = requests.post('http://127.0.0.1:8000/data/', data=json.dumps(payload))

    r = urllib2.urlopen("http://127.0.0.1:8000/search/?quant=10&qType=3&username=david&lat=0&lon=0").read()
    l = json.loads(r)
    for i in l:
        print i['lat'],i['lon'],i['username'], i['dist'], i['name']

    #print r
