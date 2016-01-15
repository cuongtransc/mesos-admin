import json
import logging
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from elasticsearch import Elasticsearch
from apscheduler.schedulers.background import BackgroundScheduler
import random
import watcher.models as models


class Watcher:
    """Class watching the log

    Class will base conditions to implement actions
    """
    actions = []
    conditions = []

    def __init__(self, config_jons, name=""):
        """Init Object base on jons config

        @param string config_jons,
        """
        logging.getLogger("apscheduler.executors.default").setLevel("ERROR")
        logging.getLogger("elasticsearch").setLevel("ERROR")
        self._running = True
        self.logger = logging.getLogger(__name__)
        self.logger.info("Loading config ...")
        self.config = json.loads(config_jons)
        self.logger.info("Create searcher...")
        self.searcher = Elasticsearch(self.config["elasticsearch"])
        self.name = name

    def stop(self):
        self._running = False

    def set_running(self, flag):
        self._running = flag

    def add_action(self, action):
        """Add action for watcher

        @param function action, is a function have only one param (response of Elasticsearch.search)
        """
        self.logger.info("add action " + action.__name__)
        self.actions.append(action)

    def add_condition(self, condition):
        """Add condition for watcher

        @param function condition, is a function have only one param (response of Elasticsearch.search) and return boolean value
        """
        self.logger.info("add condition " + condition.__name__)
        self.conditions.append(condition)

    def add_send_gmail_action(self):
        """Action built-in class Watcher, send gmail action"""

        def send_gmail_action(response, watcher_name):
            msg = MIMEText(self.config["actions"]["gmail"]["msg"].format(response=response), 'plain')
            msg['Subject'] = 'NBC Watcher Notification'
            msg['From'] = self.config["actions"]["gmail"]["from"]["user"]
            msg['To'] = self.config["actions"]["gmail"]["to"]["user"]

            gmail = smtplib.SMTP('smtp.gmail.com:587')
            gmail.ehlo()
            gmail.starttls()
            gmail.login(self.config["actions"]["gmail"]["from"]["user"],
                        self.config["actions"]["gmail"]["from"]["pass"])
            gmail.sendmail(self.config["actions"]["gmail"]["from"]["user"],
                           self.config["actions"]["gmail"]["to"]["user"], msg.as_string())
            gmail.quit()

        self.add_action(send_gmail_action)

    def add_send_log_action(self):
        def send_log_action(response):
            self.logger.info(self.config["actions"]["log"]["format"].format(response=response))

        self.add_action(send_log_action)

    def watching(self):
        """Query log in elasticsearch and compare condition then implement action"""
        self.logger.info("Searching in elasticsearch...")
        print("Searching in elasticsearch...")
        response = self.searcher.search(index=self.config["index"], body=self.config["search"])
        self.logger.debug("Total hits: " + str(response['hits']['total']))
        self.logger.debug(response)

        result = True
        self.logger.debug("Checking conditions...")
        for condition in self.conditions:
            result = result and condition(response)

        self.logger.debug("Result = " + str(result))
        if (result == True):
            for action in self.actions:
                try:
                    self.logger.debug("Implement action " + action.__name__)
                    action_thread = threading.Thread(target=action, args=(response,self.name), daemon=True)
                    action_thread.start()
                except Exception as e:
                    self.logger.error(e)

    def run(self):
        """Run watcher"""
        self.logger.info("Running watcher ...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.watching, 'interval', seconds=self.config["interval"])
        scheduler.start()
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while self._running:
                time.sleep(2)
            scheduler.shutdown()
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()

def total_condition(response):
    return response['hits']['total'] > 0

def store_in_db_action(response, watcher_name):
    try:
        notification = models.Notification()
        notification.title = "Error"
        notification.message = "Total error "+str(response['hits']['total'])
        notification.watcher = models.Watcher.objects.get(name=watcher_name)
        notification.save()
    except Exception as e:
        print(str(e))


class WatcherThread(threading.Thread):
    def __init__(self, name, watcher):
        threading.Thread.__init__(self)
        self.setName(name)
        self.watcher = watcher
        self.setDaemon(True)
        self.watcher.add_condition(total_condition)
        self.watcher.add_action(store_in_db_action)
        self.watcher.add_send_gmail_action()

    def run(self):
        self.watcher.run()

    def stop(self):
        self.watcher.stop()
