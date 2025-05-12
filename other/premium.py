import disnake
import os
import yoomoney

from disnake.ext import commands
from dotenv import load_dotenv

from database.guild import Guild

load_dotenv()

YOOMONEY_TOKEN = os.getenv('YOOMONEY_TOKEN')
YOOMONEY_WALLET = os.getenv('YOOMONEY_WALLET')
client = yoomoney.Client(YOOMONEY_TOKEN)

class BuyPremium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()


    @commands.slash_command(name='premium', description='Купить премиум')
    async def premium(self, inter):

        pyment_id = str(inter.author.id)

        pyment_url = f'https://yoomoney.ru/quickpay/confirm.xml?receiver={YOOMONEY_WALLET}&quickpay-form=button&paymentType=AC&sum=3&label={pyment_id}&targets=PREMIUM'

        embed = disnake.Embed(title='Покупка премиум',
            description=f'Сумма: 300₽ PREMIUM STATUS',
            color=disnake.Color.light_gray()     
        )
        embed.add_field(name='> Ссылка на оплату', value=f'[Оплатить]({pyment_url})')
        await inter.response.send_message(embed=embed)
        
    async def check_pement(self, pyment_id, inter):
        history = client.operation_history(label=pyment_id)
        for operation in history.operations:
            if operation.status == 'success':
                embed = disnake.Embed(title='Успешно', description=f'Оплата ({300}₽) прошла успешно')
                await inter.send(embed=embed)
                self.db.susse_premium(inter.guild.id)
        return False

def setup(bot):
    bot.add_cog(BuyPremium(bot))