# -*- coding: utf-8 -*-

import logging
import logging.handlers
import pathlib

from telegram.ext import Updater, JobQueue
from telegram.ext import ApplicationBuilder

import config
from blackjackbot import handlers, error_handler
from blackjackbot.gamestore import GameStore

logdir_path = pathlib.Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("bot.log")

if not logdir_path.exists():
    logdir_path.mkdir()

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

loglevels = {"debug": logging.DEBUG, "error": logging.DEBUG, "fatal": logging.FATAL, "info": logging.INFO}
loglevel = loglevels.get(config.LOGLEVEL, logging.INFO)

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel, handlers=[logfile_handler, logging.StreamHandler()])
logging.getLogger("telegram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

updater = ApplicationBuilder().token(config.BOT_TOKEN).build()

for handler in handlers:
    updater.add_handler(handler)

updater.add_error_handler(error_handler)

# Set up jobs
def stale_game_cleaner(context):
    gs = GameStore()
    gs.cleanup_stale_games()


updater.job_queue.run_repeating(callback=stale_game_cleaner, interval=300, first=300)


updater.run_polling()
logger.info("Started polling!")
   

logger.info("Bot started as @{}".format(updater.bot.username))
updater.idle()
