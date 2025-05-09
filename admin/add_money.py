import disnake

from disnake.ext import commands

from database.guild import Guild

class AddMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='add-money', description='Выдать пользователю деньги')
    async def add_money(self, inter, участник: disnake.Member = commands.Param(description='Укажите участника'), сколько: int = commands.Param(description='Сколько денег выдать')):
        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        users = guild_info['economy']['users']

        if сколько <= 0: return await inter.response.send_message('Вы не можете выдать меньше 0', ephemeral=True)
        if участник.bot: return await inter.response.send_message('Вы не можете выдать деньги боту', ephemeral=True)
        embed = disnake.Embed(title=f'Уведомление',
            description=f'На ваш счет поступило - `{сколько}`\nАдминистратор {inter.author.mention} выдал вам денег'
        )
        await участник.send(embed=embed)
        self.db.add_money(inter.guild.id, участник.id, сколько)
        await inter.response.send_message('Вы успешно выдали деньги', ephemeral=True)




def setup(bot):
    bot.add_cog(AddMoney(bot))