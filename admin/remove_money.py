import disnake

from disnake.ext import commands

from database.guild import Guild

class  RemoveMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='remove-money', description='Забрать у пользователя деньги')
    async def remove_money(self, inter, участник: disnake.Member = commands.Param(description='Укажите участника'), сколько: int = commands.Param(description='Сколько денег выдать')):
        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        users = guild_info['economy']['users']
        user = users.get(str(участник.id), {})

        if сколько <= 0: return await inter.response.send_message('Вы не можете забрать меньше 0', ephemeral=True)
        if участник.bot: return await inter.response.send_message('Вы не можете выдать деньги боту', ephemeral=True)
        if user.get('balance') <= 0: return await inter.response.send_message('Вы не можете забрать деньги у пользователя когда его баланс равен 0 или меньше')
        if inter.author.guild_permissions.administrator:
            embed = disnake.Embed(title=f'Уведомление',
                description=f'С вашего баланся забрали - `{сколько}`\nАдминистратор {inter.author.mention} забрал у вас денги'
            )
            await участник.send(embed=embed)
            self.db.add_money(inter.guild.id, участник.id, сколько)
            await inter.response.send_message('Вы успешно забрали денги', ephemeral=True)
        else:
            await inter.response.send_message('Вы не являетесь администратором', ephemeral=True)

def setup(bot):
    bot.add_cog(RemoveMoney(bot))