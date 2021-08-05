import os
import time
from loguru import logger

# 日志收集器
LOG_FOLDER = os.getcwd() + '\\logs'
if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)
t = time.strftime("%m_%d_%H")

logger = logger
logger.remove(handler_id=None)  # 禁用控制台输出
logger.add("{}\\log_{}.log".format(LOG_FOLDER, t), format="{message}",
           rotation="1 day", encoding="utf-8", retention="300 days")
