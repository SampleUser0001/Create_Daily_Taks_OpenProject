# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG
import os

import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util
from controller import CreateTaskController

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

def exec():
    args = sys.argv
    args_index = 1
    
    task_date = args[args_index]; args_index += 1
    logger.debug(f"task_date: {task_date}")
    
    controller = CreateTaskController()
    controller.create_task(task_date)
    
if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    logger.info('Daily Task Create Start!!')
    exec()
    logger.info('Daily Task Create Finish!!')