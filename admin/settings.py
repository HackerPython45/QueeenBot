import disnake
import asyncio

from datetime import datetime
from disnake.ext import commands

from database.guild import Guild


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Guild()

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name='settings', description='Настройки бота')
    async def settings(self, inter):
        if inter.author.guild_permissions.administrator:
            guild_info = self.db.find_one({"guild_id": inter.guild.id})
            settings_info = guild_info['settings']
            find_channel = inter.guild.get_channel(settings_info.get('channel_id_message', 1))
            find_channel_welcome = inter.guild.get_channel(settings_info.get('welcome_channel_id', 1))
            embed = disnake.Embed(title='Настройки')
            embed.add_field(name='', value=f'Анти-бот: {"вкл ✅" if settings_info.get("antibot", 1) == 1 else "выкл ❌"}', inline=False)
            embed.add_field(name='', value=f'Анти-Линк: {"вкл ✅" if settings_info.get("antilink", 1) == 1 else "выкл ❌"}', inline=False)
            embed.add_field(name='', value=f'Канал логов: {f"{find_channel.mention}" if find_channel else "Не установлено"}', inline=False)
            embed.add_field(name='', value=f'Канал приветствий: {f"{find_channel_welcome.mention}" if find_channel_welcome else "Не установлено"}', inline=False)
            await inter.response.send_message(embed=embed, view=SettingsButton(settings_info))


class SettingsButton(disnake.ui.View):
    def __init__(self, settings_info):
        super().__init__(timeout=None)
        self.settings_info = settings_info
        self.db = Guild()
        self.antilink = settings_info.get('antilink', 1)
        self.antibot = settings_info.get('antibot', 1)
        self.welcome = settings_info.get('welcome_channel_id', 1)


        self.add_item(self.create_anti_bot_button())
        self.add_item(self.create_anti_link_button())
        self.add_item(self.channel_send_message())
        self.add_item(self.welcome_channel_button())


    def create_anti_bot_button(self):
        button = disnake.ui.Button(
            label='Анти-Бот',
            style=disnake.ButtonStyle.danger if self.antibot == 1 else disnake.ButtonStyle.success,
            custom_id="anti_bot_button"
        )
        button.callback = self.anti_bot_button
        return button

    def create_anti_link_button(self):
        button = disnake.ui.Button(
            label='Анти-Линк',
            style=disnake.ButtonStyle.danger if self.antilink == 1 else disnake.ButtonStyle.success,
            custom_id="anti_link_button"
        )
        button.callback = self.anti_link_button
        return button

    def channel_send_message(self):
        button = disnake.ui.Button(label='Канал для логов', style=disnake.ButtonStyle.gray, row=1, custom_id='channel_id_send')
        button.callback = self.channel_send_callback
        return button
    
    def welcome_channel_button(self):
        button = disnake.ui.Button(label='Приветствие', style=disnake.ButtonStyle.gray, custom_id='welcome_button_callback', row=1)
        button.callback = self.welcome_button_callback
        return  button
    
    async def welcome_button_callback(self, inter: disnake.Interaction):
        view = disnake.ui.View()
        view.add_item(ChannelSelectWelcome())
        await inter.response.send_message(embed=disnake.Embed(description='Выберите канал'), view=view, ephemeral=True)

    async def channel_send_callback(self, inter: disnake.Interaction):
        view = disnake.ui.View()
        view.add_item(ChannelSelect())
        await inter.response.send_message('Выберите канал', view=view, ephemeral=True)

    async def anti_bot_button(self, inter: disnake.Interaction):
        new_status = 1 if self.antibot == 0 else 0
        self.db.antibot_enable(inter.guild.id, new_status)

        embed = inter.message.embeds[0]
        embed.set_field_at(0, name='', value=f'Анти-бот: {"вкл ✅" if new_status == 1 else "выкл ❌"}', inline=False)
        
        self.antibot = new_status

        # Обновляем стиль кнопки
        for child in self.children:
            if child.custom_id == "anti_bot_button":
                child.style = disnake.ButtonStyle.danger if new_status == 1 else disnake.ButtonStyle.success

        await inter.response.edit_message(embed=embed, view=self)

    async def anti_link_button(self, inter: disnake.Interaction):
        new_status = 1 if self.antilink == 0 else 0
        self.db.antilink_enable(inter.guild.id, new_status)

        embed = inter.message.embeds[0]
        embed.set_field_at(1, name='', value=f'Анти-линк: {"вкл ✅" if new_status == 1 else "выкл ❌"}', inline=False)
        
        self.antilink = new_status

        # Обновляем стиль кнопки
        for child in self.children:
            if child.custom_id == "anti_link_button":
                child.style = disnake.ButtonStyle.danger if new_status == 1 else disnake.ButtonStyle.success

        await inter.response.edit_message(embed=embed, view=self)

class ChannelSelect(disnake.ui.ChannelSelect):
    def __init__(self):
        self.db = Guild()
        super().__init__(
            placeholder="Выберите канал",
            channel_types=[disnake.ChannelType.text],  # Только текстовые каналы
            max_values=1,
            min_values=1,
            custom_id="channel_select_send"
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        # Получаем выбранный канал
        selected_channel = inter.values[0]
        self.view.selected_channel = selected_channel
        
        guild_info = self.db.find_one({'guild_id': inter.guild.id})
        settings_info = guild_info['settings']
        find_channel = inter.guild.get_channel(settings_info.get('channel_id_message', 1))
        channel_id = 1 if settings_info.get('channel_id_message', 1) == 0 else 0

        self.db.set_channel_id_message(inter.guild.id, int(selected_channel))
        
        # Отправляем подтверждение
        await inter.response.send_message(
            f'Вы успешно установили канал логов: <#{int(selected_channel)}>',
            ephemeral=True
        )

class ChannelSelectWelcome(disnake.ui.ChannelSelect):
    def __init__(self):
        self.db = Guild()
        super().__init__(placeholder='Выберите канал', channel_types=[disnake.ChannelType.text], max_values=1, min_values=1, custom_id='channel_select_welcome')

    async def callback(self, inter: disnake.MessageInteraction):
        select_channel = inter.values[0]
        self.view.select_channel = select_channel

        guild_info = self.db.find_one({"guild_id": inter.guild.id})
        settings_info = guild_info['settings']

        channel_id = 1 if settings_info.get('welcome_channel_id', 1) == 0 else 0

        self.db.set_channel_id_welcome(inter.guild.id, int(select_channel))

        await inter.response.send_message(embed=disnake.Embed(description=f'Вы успешно устоновили - <#{int(select_channel)}> канал для приветствие'), ephemeral=True)

def setup(bot):
    bot.add_cog(Settings(bot))