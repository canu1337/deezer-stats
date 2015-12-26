from time import strftime, gmtime
import urllib
import Config as c
from flask import render_template, request, Flask, url_for, redirect
from pony.orm import db_session, select, count
from pony import orm
from Model import Track, Artist, History_Entry, db

app = Flask(__name__)
app.debug = True

@app.route("/")
@db_session
def index():
    orm.sql_debug(True)
    since = select(e.timestamp for e in History_Entry).min()
    top_songs = select((t.title, count(t.entries)) for t in Track).order_by(-2)[:10]
    #who the fuck wrote this, order_by(-2) means we order by count(t.entries) descending
    ta = select((a.name, count(t.entries)) for t in Track for a in t.artist).order_by(-2)[:10]
    total_tracks = select((count(t.entries), t.duration) for t in Track)[:]
    #cant sum(count(t.entries * t.duration))
    total_listened = 0
    for track in total_tracks:
        total_listened += track[0] * track[1]
    return render_template('stats.html', top = top_songs, top_artist = ta, total = strftime('%-H hours %-M minutes %-S seconds',gmtime(total_listened)), date = since)

@app.route("/login")
def login():
    return redirect('https://connect.deezer.com/oauth/auth.php?app_id=' + c.APP_ID + '&redirect_uri='+ c.LOGIN_REDIRECT_URL +'&perms=basic_access,listening_history,offline_access', code  = 302)


@app.route("/login/done")
def get_token():
    if request.args.get('error_reason') != None:
        return "Error " + request.args.get('error_reason')
    else:
        response = urllib.urlopen('https://connect.deezer.com/oauth/access_token.php?app_id=' + c.APP_ID + '&secret=' + c.APP_SECRET + '&code=' + request.args.get('code'))
        token = response.read()
        token = token.split('=')[1][:-8]
        f = open('token', 'w')
        f.write(token)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=1234)