from django.core.management.base import BaseCommand
from django.conf import settings

import asyncio
from asgiref.sync import sync_to_async

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

from ugc.models import Profile, Message


def log_errors(f):

    async def inner(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:

            error_message = f'An error has occurred: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
async def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = await sync_to_async(Profile.objects.get_or_create, thread_sensitive=True)(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = await sync_to_async(Message, thread_sensitive=True)(
        profile=p,
        text=text,
    )
    await sync_to_async(m.save, thread_sensitive=True)()

    await update.message.reply_text(
        text=f"Your ID = {chat_id}\nMessage ID = {m.pk}\n{text}",
    )


@log_errors
async def do_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    p, _ = await sync_to_async(Profile.objects.get_or_create, thread_sensitive=True)(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = await sync_to_async(Message.objects.filter, thread_sensitive=True)(profile=p)
    count = await sync_to_async(m.count, thread_sensitive=True)()

    await update.message.reply_text(
        text=f'You have {count} posts',
    )


async def bot_get_me(app):
    print(await app.bot.get_me())


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        app = ApplicationBuilder().token(settings.TOKEN).build()

        asyncio.ensure_future(bot_get_me(app))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, do_echo))
        app.add_handler(CommandHandler('count', do_count))

        app.run_polling()
