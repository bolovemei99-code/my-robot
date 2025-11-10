import os

# Load the TOKEN with os.environ
TG_TOKEN = os.environ.get('TG_TOKEN')

# Use TG_TOKEN in the rest of the program instead of hardcoded tokens.

# Example of using TG_TOKEN
# (Assuming there's some function to send messages)
# send_message(TG_TOKEN, message)  # Modify as needed

# ... (rest of your main.py code without hardcoded BOT_TOKENs)