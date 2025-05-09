import disnake

from disnake.ext import commands

from database.guild import Guild

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.slash_command(name="profile", description="Посмотреть профиль")
    async def profile(self, inter: disnake.ApplicationCommandInteraction, участник: disnake.Member = None):
        участник = участник or inter.author
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        users = guild_info['economy']['users']
        if участник.bot: return await inter.response.send_message('Вы не можете посмотреть профиль бота', ephemeral=True)
        if not  guild_info:
            return await inter.response.send_message('Не найдено в БД', ephemeral=True)

        users_data = users.get(str(участник.id), {})
        embed = disnake.Embed(title=f'Профиль -> {участник.name}')
        embed.add_field(name='', value=f'💵 | Баланс: {users_data.get("balance", 0)}', inline=False)
        embed.add_field(name='', value=f'🏛️ | Банк: {users_data.get("bank", 0)}', inline=False)
        embed.add_field(name='', value=f'📊 | Уровень: {users_data.get("level", 0)}', inline=False)
        embed.add_field(name='', value=f'⭐ | EXP: {users_data.get("exp", 0)}', inline=False)
        embed.add_field(name='', value=f'⚠️ | warn: {users_data.get("warn", 0)}/4', inline=False)
        embed.set_footer(text=inter.author.name, icon_url=inter.author.avatar.url)
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))