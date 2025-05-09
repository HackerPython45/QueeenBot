import disnake
import random
import asyncio

from disnake.ext import commands
from datetime import datetime, timedelta

from database.guild import Guild

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.cooldown(1, 10800)
    @commands.slash_command(name='work', description='Работать')
    async def work(self, inter):
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        users_info = guild_info['economy']['users']
        author = users_info.get(str(inter.author.id), {})

        bonus = random.randint(150, 500)

        self.db.timely(inter.guild.id, inter.author.id, bonus)
        embed = disnake.Embed(title='Работа', 
            description=f'Вы заработали {bonus}, возвращайтесь через 3 часа'
        )
        await inter.response.send_message(embed=embed)
        await self.start_time_work(inter.author)

    async def start_time_work(self, user):
        timely_timer = 10800
        await asyncio.sleep(int(timely_timer))

        embed = disnake.Embed(title='Уведомление',
        description=f'Пора заканчивать отдыхать, пора  на выходить на работу\n`/work` - Начни зарабатывать большие деньги')
        await user.send(embed=embed)


    @work.error
    async def timely_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            retry_after = timedelta(seconds=error.retry_after)
            time_left = str(retry_after).split('.')[0]
            await inter.response.send_message(f'Вы сегодня уже работали, приходите через -> {time_left}', ephemeral=True)
        else:
            raise error

def setup(bot):
    bot.add_cog(Work(bot))