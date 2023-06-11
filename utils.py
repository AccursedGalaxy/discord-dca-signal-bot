import asyncio

def loading_message(func):
    async def wrapper(message, args):
        loading_message = await message.channel.send('Loading...')
        try:
            await func(message, args)
        finally:
            await loading_message.delete()
    return wrapper

