import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger("RotatingLogger")
logger.setLevel(logging.DEBUG)


handler = TimedRotatingFileHandler("daily_logs.log", when="midnight", interval=1, backupCount=7)
handler.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")
