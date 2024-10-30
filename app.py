from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Your bot's API token
API_TOKEN = "7712603902:AAHGFpU5lAQFuUUPYlM1jbu1u6XJGgs15Js"

async def start(update: Update, context: CallbackContext) -> None:
    """Start command handler with a welcome message."""
    welcome_message = (
        "Hey! Welcome to Gray Zero Bot.\n\n"
        "This bot allows you to interact with various scripts and automation tools.\n"
        "Use /scripts to view the list of available scripts you can use."
    )
    await update.message.reply_text(welcome_message)

async def show_scripts(update: Update, context: CallbackContext) -> None:
    """Show a list of scripts accepted by the bot."""
    scripts_list = """
Accepted scripts:
1. Circle
2. MemeFi
3. Booms
4. Cherry Game
5. Paws
6. Seed
7. Blum
"""
    await update.message.reply_text(scripts_list)

def main():
    """Main function to run the bot."""
    application = ApplicationBuilder().token(API_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scripts", show_scripts))

    application.run_polling()

if __name__ == '__main__':
    main()
