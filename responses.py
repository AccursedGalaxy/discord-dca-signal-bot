import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hello!"

    if message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "I can't help you."

    if p_message == "!dca":
        return "I can respond to the DCA command."

    return "I don't understand you."

