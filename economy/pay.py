import disnake


from disnake.ext import commands

from database.guild import Guild

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.slash_command(name='pay', description='Перевести деньги пользователю')
    async def pay(self, inter, сколько: int = commands.Param(description='Сколько хотите передать'), участник: disnake.Member = commands.Param(description='Какому участнику передать')):
        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        users = guild_info['economy']['users']
        author = users.get(str(inter.author.id), {})

        if участник.bot: return await inter.response.send_message('Вы не можете передать деньги боту', ephemeral=True)
        if author.get('balance', 0) <= сколько: return await inter.response.send_message('Вы не можете передать деньги меньше чем ваш баланс', ephemeral=True)
        if сколько <= 0: return await inter.response.send_message('Вы не можете передать 0 или меньше', ephemeral=True)
        embed = disnake.Embed(title='Перевод денег')
        embed.add_field(name=f'Отправитель: ', value=f'{inter.author.mention}', inline=True)
        embed.add_field(name=f'Получатель: ', value=f'{участник.mention}', inline=True)
        embed.add_field(name='Отправил: ', value=f'`{сколько}`', inline=False)
        embed.set_footer(text=inter.author.name, icon_url=inter.author.avatar.url)
        self.db.pay(inter.guild.id, inter.author.id, участник.id, сколько)
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Pay(bot))