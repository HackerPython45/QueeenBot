import disnake
import asyncio

from disnake.ext import commands
from datetime import datetime, timedelta

from database.guild import Guild


class SystemTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='system-ticket', description='Система тикетов')
    async def system_ticket(self, inter):
        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        ticket = guild_info['ticket']['channel_button']
        find_guild = self.bot.get_guild(inter.guild.id)
        find_channel = find_guild.get_channel(int(ticket))
        if inter.author.guild_permissions.administrator:

            if find_channel: return await inter.response.send_message(f'У вас уже есть система тикетов - <#{find_channel}>')
            embed = disnake.Embed(title='Настройки тикета',
                description=f'Если вы хотите добавить систему тикетов для вашего сервера, смело нажимай на кнопку **Создать**')
            await inter.response.send_message(embed=embed,view=TicketButton(self.bot))
        else:
            await inter.response.send_message('Вы не являетесь администратором')

class TicketButton(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()
        super().__init__(timeout=None)

    @disnake.ui.button(label='Создать', style=disnake.ButtonStyle.green, row=0)
    async def create_ticket(self, button: disnake.Button, inter: disnake.Interaction):
        try:
            # Создаем категорию для кнопки тикетов
            control_category = await inter.guild.create_category(
                name="Управление тикетами",
                position=0,
                reason=f"Создание системы тикетов по запросу {inter.author}"
            )
            
            # Создаем категорию для самих тикетов
            tickets_category = await inter.guild.create_category(
                name="Тикеты",
                position=1,
                reason=f"Создание системы тикетов по запросу {inter.author}"
            )
            
            # Настраиваем права для категории с тикетами
            await tickets_category.set_permissions(
                inter.guild.default_role,
                read_messages=False,
                send_messages=False
            )
            
            # Создаем канал для кнопки создания тикетов
            control_channel = await control_category.create_text_channel(
                name="создать-тикет",
                topic="Канал для создания новых тикетов"
            )
            
            # Сохраняем ID канала в базу данных
            self.db.set_channel_open_ticket(inter.guild.id, str(control_channel.id))
            # Отправляем сообщение с кнопкой создания тикетов
            embed = disnake.Embed(
                title="Создать тикет",
                description="Нажмите на кнопку ниже, чтобы создать новый тикет",
                color=disnake.Color.green()
            )
            
            await control_channel.send(
                embed=embed,
                view=CreateTicketView(self.bot, tickets_category)
            )
            
            await inter.response.send_message(
                "Система тикетов успешно создана!",
                ephemeral=True
            )
            
        except disnake.Forbidden:
            await inter.response.send_message(
                "❌ У бота нет необходимых прав!",
                ephemeral=True
            )
        except Exception as e:
            await inter.response.send_message(
                f"❌ Произошла ошибка: {str(e)}",
                ephemeral=True
            )

class CreateTicketView(disnake.ui.View):
    def __init__(self, bot, tickets_category):
        self.bot = bot
        self.tickets_category = tickets_category
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Создать тикет", style=disnake.ButtonStyle.blurple, emoji="📩")
    async def create_ticket(self, button: disnake.Button, inter: disnake.Interaction):
        # Здесь будет логика создания отдельных тикет-каналов
        pass

def setup(bot):
    bot.add_cog(SystemTicket(bot))