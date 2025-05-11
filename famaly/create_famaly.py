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
        if fam_info:
            find_leader = fam_info.get('leader', 'неизвестный лидер')
            return await inter.response.send_message(f'[Ошибка] Уже есть такая семья с таким названием, Лидер семьи: <@{find_leader}>', ephemeral=True)
        
        if not find_channel.get('new_fam_channel', 0):
            return await inter.response.send_message(f'[Ошибка] В данный момент создание семьи отключено, обратитесь в Создателю сервера что бы включил', ephemeral=True)


        embed = disnake.Embed(title='Заявка на создание семьи')
        embed.add_field(name='> Подал: ', value=f'{inter.author.name} | {inter.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{название}`', inline=False)
        channel = inter.guild.get_channel(find_channel.get('new_fam_channel', 0))
        author = inter.author
        if channel:
            await channel.send(embed=embed, view=AcceptFam(название, author))
        else:
            return False
        

class AcceptFam(disnake.ui.View):
    def __init__(self, название, author):
        super().__init__(timeout=None)
        self.db = Famaly()
        self.название = self.name
        self.author
        self.add_item(self.Acceptfamaly())
        self.add_item(self.CloseFamalt())


    def Acceptfamaly(self):
        button = disnake.ui.Button(label='Одобрить', style=disnake.ButtonStyle.green, row=0)
        button.accept_fam_button
        return button
    
    def CloseFamalt(self):
        button = disnake.ui.Button(label='Отказать', style=disnake.ButtonStyle.red, row=0)
        button.close_fam_button
        return button
    
    async def accept_fam_button(self, inter):
        embed = inter.message.embeds[0]
        embed = disnake.Embed(title='Заявка на создание семьи [✅ Одобрено]')
        embed.add_field(name='> Подал: ', value=f'{self.author.name} | {self.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{self.название}`', inline=False)
        await inter.response.edit_message(embed=embed)
        self.db.create_fam(self.author.id, self.название)
        await inter.response.send_message('[Успешно] Вы успешно ответили на зявку', ephemeral=True)
        await self.author.send(f'Ваша заявка на создание семьи [{self.название}] была одобрена')
        
    async def close_fam_button(self, inter):
        embed = inter.message.embeds[0]
        embed = disnake.Embed(title='Заявка на создание семьи [❌ Отказана]')
        embed.add_field(name='> Подал: ', value=f'{self.author.name} | {self.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{self.название}`', inline=False)
        await inter.response.edit_message(embed=embed)
        await inter.response.send_message('[Успешно] Вы успешно ответили на зявку', ephemeral=True)
        await self.author.send(f'Ваша заявка на создание семьи [{self.название}] была отказана')


def setup(bot):
    bot.add_cog(CreateFamaly(bot))