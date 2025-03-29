import botpy
from botpy.message import GroupMessage, Message, DirectMessage, C2CMessage
import os
from botpy.ext.cog_yaml import read
from gpt import *
from tools import *

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

AI = GPT("api_token")

image_kws = ["random", "image", "随机图片", "图片", "random image", "art"]


class MyClient(botpy.Client):
    # use the GPT to response
    global AI

    # channel dm
    async def on_direct_message_create(self, message: DirectMessage):
        if any([x in message.content for x in image_kws]):
            await message.reply(
                content="",
                file_image=random_file(),
            )
            return
        reply = AI.ask(message.content)
        await message.reply(content=reply)

    # channel at
    async def on_at_message_create(self, message: Message):
        if any([x in message.content for x in image_kws]):
            await message.reply(
                content="",
                file_image=random_file(),
            )
            return
        reply = AI.ask(message.content)
        await message.reply(content=reply)
        return

    # chat group at
    async def on_group_at_message_create(self, message: GroupMessage):
        if any([x in message.content for x in image_kws]):
            file_base64 = b64_img(random_file())
            uploadMedia = await message._api.post_group_base64file(
                group_openid=message.group_openid,
                file_type=1,
                file_data=file_base64,
            )
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=uploadMedia,
            )
            return
        reply = AI.ask(message.content)
        await message.reply(content=reply)


intents = botpy.Intents(
    public_guild_messages=True, direct_message=True, public_messages=True
)
client = MyClient(intents=intents)
client.run(appid=test_config["appid"], secret=test_config["secret"])
