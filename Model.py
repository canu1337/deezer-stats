from datetime import datetime
from pony.orm import Database, Required, Set

db = Database('sqlite', 'db.db', create_db=True)
class Track(db.Entity):
    deezer_id = Required(int)
    title = Required (str)
    duration = Required(int)
    artist = Required("Artist")
    bpm = Required(float)
    entries = Set('History_Entry')


class Artist(db.Entity):
    deezer_id = Required(int)
    name = Required(str)
    tracks = Set(Track)

class History_Entry(db.Entity):
    track = Required(Track)
    timestamp = Required(datetime)


db.generate_mapping(create_tables=True)