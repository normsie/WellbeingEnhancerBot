import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

TG_API_TOKEN = ""
# Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Stages
CHOICE, SECOND = range(2)
# Callback data
SLEEP, SMOKING = range(2)


# Define a few command handlers
def start(update, context):
    """Send a message when the command /start is issued"""
    # update.message.reply_text("Hello world!\nTODO:Enter captivating statement, false promises, and high hopes.")

    # The keyboard is a list of button rows, where each row is a list
    keyboard = [
        [InlineKeyboardButton("Sleep more", callback_data=str(SLEEP)),
         InlineKeyboardButton("Reduce Smoking", callback_data=str(SMOKING))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Which habit do you want to work on?",
        reply_markup=reply_markup
    )
    # TEll ConversationHandler that we're in state 'CHOICE' now
    return CHOICE
    ## Future Reference
    # user = update.message.from_user {Get user - can obtain his/her details through this object}


def sleep(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    query.message.reply_text(
        text="So you wanna sleep more? That's a perfect choice. Who wants to be Elon Musk eh :/"
    )

    keyboard = [
        [InlineKeyboardButton("Morning", callback_data=str(SLEEP)), # TODO Enter sleep code and replace callback data
         InlineKeyboardButton("Evening", callback_data=str(SMOKING))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text="How is your sleep?",
        reply_markup=reply_markup
    )
    # query.edit_message_text(
    #     text="First CallbackQueryHandler, Choose a route",
    #     reply_markup=reply_markup
    # )
    return SECOND


def smoke(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("1", callback_data=str(SLEEP)),
         InlineKeyboardButton("3", callback_data=str(SMOKING))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route",
        reply_markup=reply_markup
    )
    return CHOICE


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="See you next time!"
    )
    return ConversationHandler.END


def help(update, context):
    """Send a message when the command /help is issued"""
    update.message.reply_text("Bad Design. Help me fuckers.")


def echo(update, context):
    """Echo the user's message"""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log errors caused by Updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot"""
    # Create the Updater and pass it your bot's token

    updater = Updater(TG_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands, answer in telegram
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Setup conversation handler with the states CHOICE and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [CallbackQueryHandler(sleep, pattern='^' + str(SLEEP) + '$'),
                     CallbackQueryHandler(smoke, pattern='^' + str(smoke) + '$')],
            SECOND: [CallbackQueryHandler(sleep, pattern='^' + str(SLEEP) + '$'),
                     CallbackQueryHandler(end, pattern='^' + str(smoke) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # On noncommand i.e. message -echo the message on telegram TODO for now
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. THis should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()