import asyncio
import hikari
import os
import logging
import yuyo
from dotenv import load_dotenv

if os.name != "nt":
    import uvloop

    uvloop.install()

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = hikari.RESTBot(
    token=os.getenv("TOKEN"),
    token_type=hikari.TokenType.BOT,
    public_key=os.getenv("PUBLIC_KEY"),
)
component_client: yuyo.ComponentClient = yuyo.ComponentClient.from_rest_bot(bot)
