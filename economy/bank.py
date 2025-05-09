import disnake


from disnake.ext import commands

from database.guild import Guild


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.slash_command(name='bank', description='Положить на бановский счет')
    async def bank(self, inter, внести: int = commands.Param(default=None, description='Сумма для внесение', min_value=1), снять: int = commands.Param(default=None, description='Сумма для снятие', min_value=1)):

        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        users = guild_info['economy']['users']
        author = users.get(str(inter.author.id), {})
        if внести is not None and снять is not None: return await inter.response.send_message("❌ Нельзя одновременно вносить и снимать!", ephemeral=True)
        if not author.get('balance', 0): return await inter.response.send_message(f'Ваш баланс: {author.get("balance", 0)}', ephemeral=True)
        if снять <= author.get('bank', 1): return await inter.response.send_message('Вы не можете снять с банка меньше чем у вас есть', ephemeral=True)
        if внести <= author.get('balance', 1): return await inter.response.send_message('Вы не можете внести в банк меньше чем у вас есть', ephemeral=True)
        if внести > author.get('balance', 1) : return await inter.response.send_message('Вы не можете положить на банк больше чем у вас на балансе', ephemeral=True)

        if внести is not None:
            self.db.inc_bank(inter.guild.id, inter.author.id, внести)
            embed = disnake.Embed(title='Операции банка')
            embed.add_field(name='', value=f'{inter.author.mention}, вы успешно положили `{внести}` на свой банковский счет')
            embed.set_thumbnail(url=inter.author.avatar.url)
            await inter.response.send_message(embed=embed, ephemeral=True)
        if снять is not None:
            self.db.un_inc_bank(inter.guild.id, снять)
            embed = disnake.Embed(title='Операции банка')
            embed.add_field(name='', value=f'{inter.author.mention}, вы успешно сняли `{снять}` со своего банковского счета')
            embed.set_thumbnail(url=inter.author.avatar.url)
            await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Bank(bot))