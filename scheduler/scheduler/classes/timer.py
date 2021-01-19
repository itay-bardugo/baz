import os
from threading import Thread, Event
from scheduler.helperes import redis as redis_helper

from scheduler.repository.timer import TimerRepository
from datetime import datetime, timedelta
import requests
import time


class StoppableTimer(Thread):
    def __init__(self, timer_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event = Event()
        self._timer_id = timer_id
        self._timer = TimerRepository.find_by_id(self._timer_id)
        self._redis_client = redis_helper.connect()

    def run(self):
        now = datetime.now()
        print('now.__str__()', now.__str__())
        print('self._timer.action_date.replace(tzinfo=None).__str__()',
              self._timer.action_date.replace(tzinfo=None).__str__())
        self._timer.thread_id = self.ident
        self._timer.status = self._timer.SETTING_UP
        self.update_timer()
        try:
            self._timer.status = self._timer.RUNNING
            self.update_timer()
            self._run()
            while not self._event.wait(10):
                self._run()
        except:
            ...

    def _run(self):
        print("{} : runnig".format(self.ident))
        self._timer.status = self._timer.RUNNING
        if self._has_stop_signal():
            self._stop()
            raise Exception("Timer stopped")

        if self._should_notify():
            self._notify()

        if self._timer.status == self._timer.FAILED:
            print("{} : Failed".format(self.ident))
            raise Exception("Timer Failed")

    def _should_notify(self):
        return datetime.utcnow() >= self._timer.action_date.replace(tzinfo=None)

    def _update_next_notification(self):
        self._timer.action_date += timedelta(seconds=self._timer.sleep_time)
        print("next schedule time is: {}".format(self._timer.action_date))

    def _notify(self):
        try:
            print("{} : trying to notify".format(self.ident))
            requests.post(self._timer.return_address, data={"param": self._timer.param})
            self._update_next_notification()
        except:
            print("{} : notify failed".format(self.ident))
            self._timer.status = self._timer.FAILED
        self.update_timer()

    def update_timer(self):
        TimerRepository.save(self._timer)

    def _has_stop_signal(self):
        return (stop := self._redis_client.mget(self._timer.signature)) and stop[0] is not None

    def _stop(self):
        print("{} : stopping...".format(self.ident))
        self._redis_client.delete(self._timer.signature)
        self._timer.status = self._timer.STOPPED
        self.update_timer()
