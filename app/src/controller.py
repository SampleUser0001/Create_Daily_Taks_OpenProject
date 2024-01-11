# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

import json
import requests

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

PARENT_TASK_FILE = ['config', 'parent_task.json']
CHILD_TASK_FILE = ['config', 'child_task.json']

DATE_FORMAT = "$date$"

API_HEADER = {"Content-Type": "application/json"}

class CreateTaskController():
    def __init__(self) -> None:
        pass
    
    def create_task(self, task_date: str) -> None:
        logger.info("create task start")
        
        parent_response = self._create_parent(task_date)       
        parent_task = self._get_task_self(parent_response)
        
        logger.info(f"parent_task: {parent_task}")
        self._create_children(parent_task, task_date)
        
        logger.debug("create task finish")

    def _create_parent(self, task_date: str) -> dict:
        """ 親タスクを作成する
        
        Args:
            task_date (str): 任意の日付フォーマット
        Returns:
            dict: 親タスク情報
        """

        with open(os.path.join(PYTHON_APP_HOME, *PARENT_TASK_FILE), "r") as file:
            parent_task = json.load(file)
        
        parent_task = self._replace_task_date(parent_task, task_date)
        response = self._call_api(parent_task)
        
        logger.debug(f"parent_task: {response}")
        
        return response

    def _create_children(self, parent: dict, task_date:str) -> None:
        """ 子タスクを作成する
        Args:
            parent (dict): 親タスク情報
            task_date (str): 任意の日付フォーマット
        """
        with open(os.path.join(PYTHON_APP_HOME, *CHILD_TASK_FILE), "r") as file:
            child_tasks = json.load(file)

        
        LINKS = "_links"
        PARENT = "parent"
        for child_task in child_tasks:
            child_task = self._replace_task_date(child_task, task_date)
            
            # 親タスクを紐付ける
            child_task[LINKS][PARENT] = parent
            response = self._call_api(child_task)
            logger.info(f"child_task: {self._get_task_self(response)}")
            logger.debug(f"child_task: {response}")

    def _replace_task_date(self, task: dict, task_date: str) -> dict:
        """ タスクの日付を置換する """
        
        SUBJECT = "subject"
        DESCRIPTION = "description"
        RAW = "raw"
        
        task[SUBJECT] = task[SUBJECT].replace(DATE_FORMAT, task_date)
        task[DESCRIPTION][RAW] = task[DESCRIPTION][RAW].replace(DATE_FORMAT, task_date)

        return task

    def _call_api(self, task: dict) -> dict:
        """ タスク作成APIを呼び出す """
        
        auth = ('apikey' , ImportEnvKeyEnum.API_KEY.value)

        response = requests.post(
            url=ImportEnvKeyEnum.ENDPOINT.value,
            headers=API_HEADER,
            data=json.dumps(task),
            auth=auth)

        return response.json()

    def _get_task_self(self, response: dict) -> dict:
        """ タスク情報からselfを取得する。ここで言うselfは作成されたタスクのURLとタイトル。 """
        
        LINKS = "_links"
        SELF = "self"
        
        return response[LINKS][SELF]
    