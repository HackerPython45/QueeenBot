import disnake
import os
import asyncio

from dotenv import load_dotenv
from disnake.ext import commands

from database.guild import Guild

load_dotenv()

db = commands.Bot(command_prefix='!', intents=disnake.Intents.all(), test_guilds=[1367450430124195900])
db.remove_command('help')

database = Guild()

@db.event
async def on_ready():
    print('-----------------------------')
    print('------Queen Бот запущен------')
    print('-----------------------------')
    for guild in db.guilds:
        check_guild = database.find_one({"guild_id": guild.id})
        if not check_guild:
            database.create_table_guild(guild)
                
@db.event
async def on_guild_join(guild):
    check_guild = database.find_one({"guild_id": guild.id})
    if not check_guild:
        database.create_table_guild(guild)

@db.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('У вас должна быть соответствующая роль для использования этой команды')
    else:
        error = await ctx.send('Команда не найдена, воспользуйтесь `/help`')
        await asyncio.sleep(3)
        await error.delete()



db.load_extension('economy.profile')
db.load_extension('economy.bank')
db.load_extension('economy.pay')
db.load_extension('economy.timely')
db.load_extension('economy.work')


db.load_extension('other.help')
db.load_extension('other.offers')
db.load_extension('other.voting')
db.load_extension('other.info')


db.load_extension('admin.ban')
db.load_extension('admin.unban')
db.load_extension('admin.kick')
db.load_extension('admin.warn')
db.load_extension('admin.unwarn')
db.load_extension('admin.add_money')
db.load_extension('admin.remove_money')
db.load_extension('admin.antibot')
db.load_extension('admin.antilink')
db.load_extension('admin.settings')
db.load_extension('admin.welcome')
db.load_extension('admin.set_reputation')

db.load_extension('progress.give_progress')

if __name__ == "__main__":
    db.run(os.getenv('token'))