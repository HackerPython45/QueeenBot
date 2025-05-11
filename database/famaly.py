import os
import disnake

from disnake.ext import commands

from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

class Famaly(object):
    conn = MongoClient(os.getenv('mongo_url'))
    db = conn.fam.famdb


    def create_famaly(self, leader: int, fam_name: str):
        if self.db.find_one({"$or": [{"leader": leader}, {"fam_name": fam_name}]}):
            return False
        create_fam = {
            'leader': leader,
            'fam_name': fam_name,
            'zam': 0,
            'rep': 0,
            'max_member': 5,
            'fam_settings': {
                'fam_channel': 0,
                'fam_voice_channel': 0
            },
            'fam_dostup': {
                'invite': 10,
                'uninvite': 10
            },
            'members': {str(leader): {
                'access_level': 1,
                'role': fam_name
            }}
        }
        try:
            self.db.insert_one(create_fam)
            return True
        except Exception as e:
            print(f'[Ошибка] Не удалось создать семью: {e}')
            return False

    def find_one(self, query):
        return self.db.find_one(query)
    

    def find(self, query):
        return self.db.find(query)

    def invite_member(self, fam_name: str, user_id: int, accesse_level: int =1, role: str = 'Участник'):
        family = self.db.find_one({"fam_name": fam_name})
        if not fam_name:
            return False

        if str(user_id) in family['members']:
            return False
        
        self.db.update_one({"fam_name": fam_name},
            {"$set": {f"members.{user_id}": {
                "accesse_level": accesse_level,
                "role": role
            }}})
        return True

    def find_one(self, query):
        return self.db.find_one(query)

    def remove_member(self, fam_name: str, user_id: int):
        self.db.update_one({"fam_name": fam_name}, {"$unset": {f"members.{user_id}": ""}})
        return True
    
    def set_member_permission(self, fam_name: str, user_id: int, new_accesse: int):
        self.db.update_one({"fam_name": fam_name}, {
            "$set": {
                f"members.{user_id}.accesse_level": new_accesse}})
        return True