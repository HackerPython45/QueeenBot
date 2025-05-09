import disnake
import random
import asyncio

from disnake.ext import commands
from datetime import datetime, timedelta

from database.guild import Guild

class Timely(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    
    @commands.slash_command(name='timely', description='Получить ежедневную награду')
    @commands.cooldown(1, 43200)
    async def timely(self, inter):
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        users_info = guild_info['economy']['users']
        author = users_info.get(str(inter.author.id), {})

        bonus = random.randint(20, 250)

        self.db.timely(inter.guild.id, inter.author.id, bonus)
        await inter.response.send_message(f'Вы успешно получить ежедневную награду в размере: {bonus}', ephemeral=True)

        await self.start_cooldown(inter.author)


    async def start_cooldown(self, user):
        timely_timer = 43200
        await asyncio.sleep(int(timely_timer))

        embed = disnake.Embed(title='Уведомление',
        description=f'Ваше КД на получение ежедневной награды прошло!\n Пропишите вновь команда `/timely` что бы получить снова награду')
        await user.send(embed=embed)


    @timely.error
    async def timely_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            retry_after = timedelta(seconds=error.retry_after)
            time_left = str(retry_after).split('.')[0]
            await inter.response.send_message(f'Вы уже получали сегодня ежедневную награду. Осталось: {time_left}', ephemeral=True)
        else:
            raise error

def setup(bot):
    bot.add_cog(Timely(bot))