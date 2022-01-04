from datetime import datetime


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello', 'hi', 'hey', 'hello!', 'hi!', 'hey!'):
        return "Hey! How's it going?"

    if user_message in ('who are you', 'who are you?'):
        return "I am an Example Bot!"

    if user_message in ('time', 'time?', 'what time is it now', 'what time is it now?', 'what time is it right now',
                        'what time is it right now?', 'what time is it', 'what time is it?', 'what is the time',
                        'what is the time?'):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        return str(date_time)

    return "I don't understand you."
