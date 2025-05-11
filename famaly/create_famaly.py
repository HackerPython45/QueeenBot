import disnake

from disnake.ext import commands
from datetime import datetime

from database.famaly import Famaly
from database.guild import Guild

class CreateFamaly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dg = Guild()
        self.db = Famaly()
        

    @commands.slash_command(name='fam-create', description='Создать семью')
    async def create_fam(self, inter, название: str = commands.Param(description='Введите название семьи', min_length=3, max_length=16)):
        fam_info = self.db.find_one({"fam_name": название})
        find_guild = self.dg.find_one({"guild_id": inter.guild.id})
        find_leader = fam_info['leader']
        find_channel = find_guild['settings']
        # if fam_info:
        #     return await inter.response.send_message(f'[Ошибка] Уже есть такая семья с таким названием, Лидер семьи: <@{find_leader}>', ephemeral=True)
        
        if not find_channel.get('new_fam_channel', 0):
            return await inter.response.send_message(f'[Ошибка] В данный момент создание семьи отключено, обратитесь в Создателю сервера что бы включил', ephemeral=True)


        embed = disnake.Embed(title='Заявка на создание семьи')
        embed.add_field(name='> Подал: ', value=f'{inter.author.name} | {inter.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{название}`', ephemeral=True)
        channel = inter.guild.get_channel(find_channel.get('new_fam_channel', 0))
        if channel:
            await channel.send(embed=embed)
        else:
            return False
        

def setup(bot):
    bot.add_cog(CreateFamaly(bot))