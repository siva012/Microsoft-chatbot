
import json,wikipedia,urllib,os
from chatbot import multiFunctionCall

app_client_id = `<Microsoft App ID>`
app_client_secret = `<Microsoft App Secret>`


def about(query,qtype=None):
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    if not len(response['itemListElement']):
        return "sorry, I don't know about "+query +"\nIf you know about "+query+" please tell me."
    result = ""
    if len(response['itemListElement'])==1:
        if "detailedDescription" in response['itemListElement'][0]['result']:
            return response['itemListElement'][0]['result']['detailedDescription']["articleBody"]
        else:
            return response['itemListElement'][0]['result']['name'] +" is a " +\
                   response['itemListElement'][0]['result']["description"]
    for element in response['itemListElement']:
      try:result += element['result']['name'] + "->" +element['result']["description"]+"\n"
      except:pass
    return result

def getType(l):
    try:
        l.remove("Thing")
        return "("+l[0]+")"
    except:
        return ""

def tellMeAbout(query,sessionID="general"):
    return about(query)

def whoIs(query,sessionID="general"):
    return about(query,qtype="Person")

def whereIs(query,sessionID="general"):
    return about(query,qtype="Place")

def whatIs(query,sessionID="general"):
    try:
        return wikipedia.summary(query)
    except:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except:
                pass
    return about(query)

call = multiFunctionCall({"whoIs":whoIs,
                          "whatIs":whatIs,
                          "whereIs":whereIs,
                          "tellMeAbout":tellMeAbout})
