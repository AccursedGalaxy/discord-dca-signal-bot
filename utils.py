def loading_message(func):
    async def wrapper(message, args):
        loading_message = await message.channel.send('Loading...')
        try:
            await func(message, args)
        finally:
            await loading_message.delete()
    return wrapper

def is_admin():
    def decorator(func):
        async def wrapper(message, args):
            if message.author.guild_permissions.manage_guild:
                await func(message, args)
            else:
                await message.channel.send("You must have the 'Manage Server' permission to use this command.")
        return wrapper
    return decorator
