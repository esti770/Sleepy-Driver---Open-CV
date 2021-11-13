import json
import os.path
import pyrebase
from datetime import datetime

FIREBASE_CONFIG = {
 ****
}


class DataBase:
    user_id: int
    _user_id_file: str = 'user_id.json'
    _firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    _db = _firebase.database()

    @classmethod
    def create_user(cls, user_id: str) -> None:
        if os.path.exists(DataBase._user_id_file) and not os.stat(DataBase._user_id_file).st_size == 0:
            return
        with open(DataBase._user_id_file, 'w') as json_file:
            json.dump(user_id, json_file)

        DataBase._db.child('users').child(user_id).set({'times':'#'})

    @classmethod
    def update_falling_asleep(cls, user_id: str, falling_asleap_time: datetime):
        history = DataBase._db.child("users").child(user_id).get().val()['times']
        update = history + '#' + str(falling_asleap_time)
        DataBase._db.child("users").child(user_id).update({'times': update})

    @classmethod
    def get_user_id(cls):
        if os.path.exists(DataBase._user_id_file) and not os.stat(DataBase._user_id_file).st_size == 0:
            f = open(DataBase._user_id_file, )
            user_id = json.load(f)
            DataBase.user_id = user_id
            return user_id
        return None

    @classmethod
    def get_user_data(cls, user_id):
        times = DataBase._db.child("users").child(user_id).get().val()['times']
        if times == '#':
            return []
        return times.split('#')


