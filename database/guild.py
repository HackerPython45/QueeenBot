import os
import disnake

from disnake.ext import commands

from pymongo import MongoClient

class Guild:

    conn = MongoClient('mongodb+srv://Serj:Sladko.wera3@cluster0.1rtw0mc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = conn.guld.gulddb


    def create_table_guild(self, guild: disnake.Guild):
        guild_data = {
            'guild_id': guild.id,
            'owner_guild': guild.owner_id,
            'economy': {
                'users': {}
            },
            'ticket': {
                'channel_open_ticket': 0,
                'category_ticket': 0
            },
            'premium': 0,
            'settings': {
                'antibot': 0,
                'antispwam': 0,
                'antilink': 0,
                'channel_id_message': 0,
                'welcome_channel_id': 0
            },
        }
        for member in guild.members:
            guild_data['economy']['users'][str(member.id)] = {
                'balance': 0,
                'level': 1,
                'exp': 0,
                'bank': 0,
                'warn': 0,
            }

        # Вставляем в базу данных
        self.db.insert_one(guild_data)



    def find_one(self, query):
        return self.db.find_one(query)
    

    def find(self, query):
        return self.db.find(query)
    
    def update_one(self, filter, update):
        return self.db.update_one(filter, update)

    def inc_bank(self, guild_id: int, user_id: int, amount: int):
        try:
            result = self.db.update_one(
                {"guild_id": guild_id},
                {"$inc": {
                    f"economy.users.{user_id}.balance": -amount,
                    f"economy.users.{user_id}.bank": amount
                }}
            )
            return result.modified_count > 0  # returns True if document was modified
        except Exception as e:
            print(f"Error updating bank: {e}")
            return False
        
    def un_inc_bank(self, guild_id: int, user_id: int, amount: int):
        self.db.update_one(
            {"guild_id": guild_id},
            {"$inc": {
                f"economy.users.{user_id}.balance": +amount,
                f"economy.users.{user_id}.bank": -amount
            }}
        )

    def pay(self, guild_id: int, user_id: int, member: int, amount: int):
        try:
            result = self.db.update_one(
                {"guild_id": guild_id},
                {"$inc": {
                    f"economy.users.{user_id}.balance": -amount,
                    f"economy.users.{member}.balance": amount
                }}
            )
            return result.modified_count > 0  
        except Exception as e:
            print(f"Error updating bank: {e}")
            return False
        
    def timely(self, guild_id: int, user_id: int, timely: int):
        self.db.update_one(
            {'guild_id': guild_id},
            {
                "$inc":
                {
                    f"economy.users.{user_id}.balance": timely
                }
            }
        )
    
    def set_warn(self, guild_id: int, user_id: int):
        self.db.update_one(
            {"guild_id": guild_id},
            {
                "$inc":
                {
                    f"economy.users.{user_id}.warn": 1
                }
            }
        )
    def dell_warn(self, guild_id: int, user_id: int):
        self.db.update_one(
            {"guild_id": guild_id},
            {
                "$inc":
                {
                    f"economy.users.{user_id}.warn": -1
                }
            }
        )

    def get_warn(self, guild_id: int, user_id: int) -> int:
    # Получаем документ гильдии
        guild_data = self.db.find_one({'guild_id': guild_id})
        
        if not guild_data:
            return 0
        
        # Получаем пользователя из economy.users
        user_data = guild_data.get('economy', {}).get('users', {}).get(str(user_id), {})
        
        # Возвращаем количество варнов или 0 если нет данных
        return user_data.get('warn', 0)
    
    def add_money(self, guild_id: int, user_id: int, money: int):
        self.db.update_one(
            {"guild_id": guild_id},
            {
                "$inc": {
                    f"economy.users.{user_id}.balance": money
                }
            })
        
    def set_channel_open_ticket(self, guild_id: int, id: int):
        self.db.update_one({"guild_id": guild_id},
            {"$inc": {
                f"ticket.channel_open_ticket": id
            }}
        )

    def antibot_enable(self, guild_id: int, status: int):
        self.db.update_one({"guild_id": guild_id},
            {'$set': {
                "settings.antibot": status
            }}                   
        )


    def antilink_enable(self, guild_id: int, status: int):
        self.db.update_one({"guild_id": guild_id},
            {'$set': {
                "settings.antilink": status
            }}                   
        )

    def set_channel_id_message(self, guild_id: int, channel: int):
        self.db.update_one({"guild_id": guild_id},
            {'$set': {
                "settings.channel_id_message": channel
            }}                   
        )

    def set_channel_id_welcome(self, guild_id: int, channel: int):
        self.db.update_one({"guild_id": guild_id},
            {'$set': {
                "settings.welcome_channel_id": channel
            }}                   
        )