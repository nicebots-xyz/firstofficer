import hikari

from config import bot

from register import create_commands
from commands import handle_command

bot.add_startup_callback(create_commands)
bot.set_listener(hikari.CommandInteraction, handle_command)

bot.run()
