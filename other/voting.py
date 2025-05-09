import disnake

from disnake.ext import commands

class VotingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='voting', description='Начать голосование')
    async def voting(self, inter):
        if inter.author.guild_permissions.administrator:
            # embed = disnake.Embed(title=название, description=описание)
            # embed.add_field(name='✅ Согласен', value='-')
            # embed.add_field(name='❌ Не согласен', value='-')
            # embed.add_field(name='❔ Не понял', value='-')
            # await inter.response.send_message(embed=embed, view=ButtonVoting())
            await inter.response.send_modal(modal=VotingModal())
        else:
            await inter.response.send_message('Вы не являетесь администратором', ephemeral=True)
        
class VotingModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Название', style=disnake.TextInputStyle.short, custom_id='name'),
            disnake.ui.TextInput(label='Описание', style=disnake.TextInputStyle.paragraph, custom_id='description'),
        ]
        super().__init__(title='Голосование', components=components)
    async def callback(self, inter):
        name = inter.text_values['name']
        description = inter.text_values['description']
        embed = disnake.Embed(title=name, description=description)
        embed.add_field(name='✅ Согласен', value='-')
        embed.add_field(name='❌ Не согласен', value='-')
        embed.add_field(name='❔ Не понял', value='-')
        await inter.response.send_message(embed=embed, view=ButtonVoting())
        await inter.before('Вы успешно сделали голосование')

class ButtonVoting(disnake.ui.View):
    def __init__(self):
        self.users = []
        self.users_id = []
        self.accept_count = 0
        self.close_count = 0
        self.what_count = 0
        super().__init__(timeout=900)
        
    @disnake.ui.button(label='✅', style=disnake.ButtonStyle.green, row=0)
    async def accept(self, button: disnake.Button, inter):
        user = inter.author.nick.split()[0] if inter.author.nick is not None else inter.author.name
        user_id = inter.author.id

        if user_id not in self.users_id:
            self.accept_count += 1
            self.users_id.append(user_id)
            self.users.append(user)
            embed = inter.message.embeds[0] if inter.message.embeds else disnake.Embed()
            embed.set_field_at(index=0, name=f'✅ Согласен({self.accept_count})', value='> \n'.join(self.users))
            await inter.message.edit(embed=embed)
            await inter.response.send_message('Вы успешно проголосовали', ephemeral=True)
        else:
            await inter.response.send_message('Вы уже проголосовали', ephemeral=True)
            
    
    @disnake.ui.button(label='❌', style=disnake.ButtonStyle.red, row=0)
    async def close(self, button: disnake.Button, inter):
        user = inter.author.nick.split()[0] if inter.author.nick is not None else inter.author.name
        user_id = inter.author.id

        if user_id not in self.users_id:
            self.close_count += 1
            self.users.append(user)
            embed = inter.message.embeds[0] if inter.message.embeds else disnake.Embed()
            embed.set_field_at(index=1, name=f'❌ Не согласен({self.accept_count})', value='\n'.join(self.users))
            await inter.message.edit(embed=embed)
            await inter.response.send_message('Вы успешно проголосовали', ephemeral=True)   
        else:
            await inter.response.send_message('Вы уже проголосовали', ephemeral=True)
            
    
    @disnake.ui.button(label='❔', style=disnake.ButtonStyle.secondary)
    async def what(self, button: disnake.Button, inter):
        user = inter.author.nick.split()[0] if inter.author.nick is not None else inter.author.name
        user_id = inter.author.id

        if user_id not in self.users_id:
            self.what_count += 1
            self.users.append(user)
            embed = inter.message.embeds[0] if inter.message.embeds else disnake.Embed()
            embed.set_field_at(index=2, name=f'❔ Не понял({self.accept_count})', value='\n'.join(self.users))
            await inter.message.edit(embed=embed)
            await inter.response.send_message('Вы успешно проголосовали', ephemeral=True)
        else:
            await inter.response.send_message('Вы уже проголосовали', ephemeral=True)
    
def setup(bot):
    bot.add_cog(VotingCommand(bot))