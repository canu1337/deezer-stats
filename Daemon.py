import urllib, json
from datetime import datetime
from pony.orm import db_session
from Model import Track, Artist, History_Entry, db

@db_session
def getHistory():
    f = open('token', 'r')
    token = f.read()
    rep = urllib.urlopen('http://api.deezer.com/user/me/history?access_token=' + token)
    data = json.loads(rep.read())
    for track in data['data']:
        if History_Entry.get(timestamp = datetime.fromtimestamp(track['timestamp'])):
            break
        if not Artist.get(deezer_id = track['artist']['id']):
            a = Artist(name=track['artist']['name'], deezer_id=track['artist']['id'])
            db.commit()
        if not Track.get(deezer_id = track['id']):
                info = urllib.urlopen('http://api.deezer.com/track/' + str(track['id']))
                track_info = json.loads(info.read())
                t = Track(title = track['title'], duration = track['duration'], artist = Artist.get(deezer_id = track['artist']['id']), bpm = track_info['bpm'], deezer_id = track['id'])
                db.commit()
        entry = History_Entry(track = Track.get(deezer_id = track['id']), timestamp = datetime.fromtimestamp(track['timestamp']))
        db.commit()

getHistory()