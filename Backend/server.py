from tornado import web, ioloop
from firebase import firebase
import json
import base64
import requests
from math import radians, sin, cos, atan2
class UserHandler(web.RequestHandler):
    def initialize(self, users,firebase):
        self.users=users
        self.firebase = firebase
    def post(self):
        """
        Args:
            username
            password
            name
        """
        info = json.loads(self.request.body)
        user = {}
        if info['username'] in self.users:
            self.clear()
            self.set_status(400)
            self.finish("User already exists")
            return
        user['username'] = info['username']
        user['password'] = info['password']
        user['name'] = info['name']
        user['preferenceData'] = {}
        self.users[user['username']] = user
        self.firebase.put('/users', user['username'], user)
        self.write("Add successful")
    def get(self):
        """
        Args:
            username
        """
        username = self.get_argument("username")
        if not username in self.users:
            self.clear()
            self.set_status(401)
            self.finish("User does not exist")
        self.write(json.dumps(users[username]))

class APIHandler(web.RequestHandler):
    def initialize(self,users,data,firebase):
        print('init')
        self.users=users
        self.data=data
        self.firebase = firebase
    def get(self):
        """
        Query for recommendations based on user.
        Information required:
            [username]
            [lat]
            [long]
            quant : how many you want
            Query Type (qType):
                1) Distance Restricted
                    Require lat+long
                2) By Rating
                3) By preference
                    Require username
        """
        def dist(lat1, lon1, lat2, lon2):
            R = 6371000.0
            l1 = radians(float(lat1))
            l2 = radians(float(lat2))
            da = radians(float(lat2-lat1))
            do = radians(float(lon2-lon1))
            a = sin(da/2)**2+cos(l1)*cos(l2)*sin(do/2)**2
            c = 2 * atan2(a**0.5, (1-a)**0.5)
            return R*c
        quant = int(self.get_argument('quant'))
        qType = int(self.get_argument('qType'))
        if qType == 1:
            lat = float(self.get_argument('lat'))
            lon = float(self.get_argument('lon'))
            items = sorted(self.data, key=lambda key: dist(self.data[key]['lat'], self.data[key]['lon'], lat, lon))
            ret = []
            for i in range(min(quant, len(items))):
                ret.append(self.data[items[i]])
                print dist(self.data[items[i]]['lat'], self.data[items[i]]['lon'], lat, lon)
            self.write(json.dumps(ret))
        elif qType == 2:
            #print 'printing selfdata0'
            #print self.data[0]
            #print self.data
            item = []
            for key in self.data:
                item.append((key, self.data[key]['rating']))
            items = sorted(item, key=lambda key: -1*key[1])
            #print items
            ret = []
            for i in range(min(quant, len(items))):
                ret.append(self.data[items[i][0]])
                print items[i][1]
            #print ret
            self.write(json.dumps(ret))
        elif qType == 3:
            username = self.get_argument('username')
            temp = []
            for key in self.data:
                tempa = 0
                for attr in self.data[key]['attributes']:
                    if attr in self.users[username]['preferenceData']:
                        tempa += self.data[key]['attributes'][attr] * self.users[username]['preferenceData'][attr]['ratingTot']/self.users[username]['preferenceData'][attr]['totalWeight']
                tempa *= -1
                temp.append((key, tempa))
            items = sorted(temp, key=lambda key: key[1])
            ret = []
            for i in range(min(quant, len(items))):
                ret.append(self.data[items[i][0]])
                print items[i][1]
            self.write(json.dumps(ret))
        print("HI")

    def post(self):
        """
        Add Image to database
        Information required:
            username
            lat
            lon
            rating
            serializedImage (base64 encoded)
        """
        info = json.loads(self.request.body)
        username = info['username']
        rating = int(info['rating'])
        lat = float(info['lat'])
        lon = float(info['lon'])

        undecode = info['serializedImage']
        print undecode

        # Clarifai Call
        headers = {"Authorization": "Bearer fvprKiHDx7UZgpvTNoONFVTqNBoyoO"}
        payload = {"encoded_data": undecode}
        r = requests.post('https://api.clarifai.com/v1/tag/', data=payload, headers=headers)
        rj = json.loads(r.text)
        print rj
        attrs = rj['results'][0]['result']['tag']['classes']
        probs = rj['results'][0]['result']['tag']['probs']
        print rj['results'][0]['result']['tag']['classes']
        print rj['results'][0]['result']['tag']['probs']

        # Create item object to place in database
        attDict = {}
        for i in range(len(attrs)):
            attDict[attrs[i]] = probs[i]
        item = {'username':username, 'rating':rating,'lat':lat, 'lon':lon, 'serializedImage':undecode, 'attributes':attDict}

        # Update database
        ## Update User
        pData = self.users[username]['preferenceData']
        for i in range(len(attrs)):
            if attrs[i] in pData:
                pData[attrs[i]]['ratingTot'] += probs[i]*(float(rating)-5.5)/4.5
                pData[attrs[i]]['totalWeight'] += probs[i]
            else:
                pData[attrs[i]] = {}
                pData[attrs[i]]['ratingTot'] = probs[i]*(float(rating)-5.5)/4.5
                pData[attrs[i]]['totalWeight'] = probs[i]
        self.firebase.put('/users/'+username, 'preferenceData', pData)

        ## Update Overall Item Data
        ret = self.firebase.post('/data', item)
        self.data[ret['name']] = item
def init(firebase):
    global users
    global data
    users = firebase.get('/users', None)
    data = firebase.get('/data', None)
    print 'Initialization done'

if __name__ ==  '__main__':
    loop = ioloop.IOLoop.instance()
    #users is indexed by username
    global users
    global data
    users = {}
    data = {}
    firebase = firebase.FirebaseApplication('https://dazzling-inferno-572.firebaseio.com/', None)
    init(firebase)
    #print users
    #print data
    application = web.Application(
        [
            (r'/data/', APIHandler, dict(users=users,data=data,firebase=firebase)),
            (r'/users/', UserHandler, dict(users=users,firebase=firebase))
        ]
    )
    application.listen(3030)
    """ Functioning Firebase Code"""
    #user = {'name':'dinosaur', 'lat':'10', 'lon': [10,234,35353]}
    #ret = firebase.post('/users', user)
    #print ret

    # f = open('test.png', 'rb')
    # undecode = base64.b64encode(f.read())
    # print undecode
    # #print undecode
    # headers = {"Authorization": "Bearer fvprKiHDx7UZgpvTNoONFVTqNBoyoO"}
    # payload = {"encoded_data": undecode}  #undecode}
    # r = requests.post('https://api.clarifai.com/v1/tag/', data=payload, headers=headers)
    # rj = json.loads(r.text)
    loop.start()
