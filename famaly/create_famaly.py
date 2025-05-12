import disnake

from disnake.ext import commands
from datetime import datetime

from database.famaly import Famaly
from database.guild import Guild

class CreateFamaly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()
        self.dg = Famaly()
        

    @commands.slash_command(name='fam-create', description='Создать семью')
    async def create_fam(self, inter, название: str = commands.Param(description='Введите название семьи', min_length=3, max_length=16)):
        find_guild = self.db.find_one({"guild_id": inter.guild.id})
        find_channel = find_guild['settings']
        find_leader = self.dg.find_one({'leader': inter.author.id})
        find_name = self.dg.find_one({"fam_name": название})
        
        if find_name:
            return await inter.response.send_message(f'Семья с таким названием уже существует', ephemeral=True)

        if not find_channel.get('new_fam_channel', 0):
            return await inter.response.send_message(f'[Ошибка] В данный момент создание семьи отключено, обратитесь в Создателю сервера что бы включил', ephemeral=True)

        if not find_leader:
            embed = disnake.Embed(title='Заявка на создание семьи')
            embed.add_field(name='> Подал: ', value=f'{inter.author.name} | {inter.author.mention}', inline=False)
            embed.add_field(name='> Название: ', value=f'`{название}`', inline=False)
            channel = inter.guild.get_channel(find_channel.get('new_fam_channel', 0))
            author = inter.author
            name = str(название)
            if channel:
                await channel.send(embed=embed, view=AcceptFam(name, author))
                await inter.response.send_message('Вы отправили заявку на создание семьи', ephemeral=True)
            else:
                return False
        else:
            return await inter.response.send_message(f'Вы уже создали семью -> {find_leader.get('fam_name')}', ephemeral=True)

class AcceptFam(disnake.ui.View):
    def __init__(self, name, author):
        super().__init__(timeout=None)
        self.db = Famaly()
        self.name = name
        self.author = author
        self.add_item(self.acceptfamaly())
        self.add_item(self.closeFamalt())


    def acceptfamaly(self):
        button = disnake.ui.Button(label='Одобрить', style=disnake.ButtonStyle.green, custom_id='accept_fam_button' ,row=0)
        button.callback = self.accept_fam_button
        return button
    
    def closeFamalt(self):
        button = disnake.ui.Button(label='Отказать', style=disnake.ButtonStyle.red, custom_id='close_fam_button', row=0)
        button.callback = self.close_fam_button
        return button
    
    async def accept_fam_button(self, inter):
        for child in self.children:
            child.disabled = True
        embed = inter.message.embeds[0]
        embed = disnake.Embed(title='Заявка на создание семьи [✅ Одобрено]')
        embed.add_field(name='> Подал: ', value=f'{self.author.name} | {self.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{self.name}`', inline=False)
        await inter.response.edit_message(embed=embed, view=self)
        self.db.create_famaly(self.author.id, self.name)
        await self.author.send(f'Ваша заявка на создание семьи [{self.name}] была одобрена')
        
    async def close_fam_button(self, inter):
        for child in self.children:
            child.disabled = True

        embed = inter.message.embeds[0]
        embed = disnake.Embed(title='Заявка на создание семьи [❌ Отказана]')
        embed.add_field(name='> Подал: ', value=f'{self.author.name} | {self.author.mention}', inline=False)
        embed.add_field(name='> Название: ', value=f'`{self.name}`', inline=False)
        await inter.response.edit_message(embed=embed, view=self)
        await self.author.send(f'Ваша заявка на создание семьи [{self.name}] была отказана')


def setup(bot):
    bot.add_cog(CreateFamaly(bot))