from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import time
from urllib.parse import urlparse, parse_qs

# Your bot's API token
API_TOKEN = "7712603902:AAHGFpU5lAQFuUUPYlM1jbu1u6XJGgs15Js"

def parse_url(url: str) -> str:
    """Parse the URL to extract the 'tgWebAppData'."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.fragment)
    return query_params.get('tgWebAppData', [None])[0]

def login_to_game(init_data: str) -> str:
    """Login to the game using the provided session link."""
    url = parse_url(init_data)
    json_data = {
        'init_data': url,
        'from': '',
        'invite_code': '',
        'is_bot': True,
    }

    # API endpoint for logging in
    login_url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
    response = requests.post(login_url, json=json_data)

    if response.status_code != 200:
        return f"Login failed: {response.text}"

    token = response.json().get('data', {}).get('access_token')
    return token

def play_game(token: str):
    """Automate gameplay by making requests to the game’s API."""
    game_id = '59bcd12e-04e2-404c-a172-311a0084587d'  # Replace with actual game ID
    headers = {'Authorization': token}

    # Start playing the game
    play_url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
    play_response = requests.post(play_url, headers=headers, json={'game_id': game_id})

    if play_response.status_code != 200:
        return f"Failed to start game: {play_response.text}"

    while True:
        time.sleep(15)  # Delay before claiming points
        claim_data = {
            'game_id': game_id,
            'points': 1000000000000000,
        }

        # Claim points
        claim_url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
        claim_response = requests.post(claim_url, headers=headers, json=claim_data)

        if claim_response.status_code == 200:
            points = claim_response.json().get('data', {}).get('points')
            if points is not None:
                return f"Points claimed successfully: {points}"
        else:
            return f"Claim failed, retrying...: {claim_response.text}"

async def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    await update.message.reply_text('Welcome! Please provide your session link.')

async def handle_session_link(update: Update, context: CallbackContext) -> None:
    """Handle the session link provided by the user."""
    session_link = update.message.text
    token = login_to_game(session_link)

    if isinstance(token, str) and token.startswith("Login failed"):
        await update.message.reply_text(token)
        return

    for i in range(10):  # Number of times to play the game
        result = play_game(token)
        await update.message.reply_text(f"Game iteration {i + 1}: {result}")

def main():
    """Main function to run the bot."""
    application = ApplicationBuilder().token(API_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_session_link))

    application.run_polling()

if __name__ == '__main__':
    main()
