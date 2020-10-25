import os
from threading import Thread, Event
from scheduler.helperes import redis as redis_helper

from scheduler.repository.timer import TimerRepository
from datetime import datetime, timedelta
import requests


class StoppableTimer(Thread):
    def __init__(self, timer_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event = Event()
        self._timer_id = timer_id
        self._timer = TimerRepository.find_by_id(self._timer_id)

    def run(self):
        now = datetime.now()
        print('now.__str__()', now.__str__())
        print('self._timer.action_date.replace(tzinfo=None).__str__()',
              self._timer.action_date.replace(tzinfo=None).__str__())
        self._timer.thread_id = self.ident
        self._timer.status = self._timer.SETTING_UP
        self._timer.sleep_time = (self._timer.action_date.replace(tzinfo=None) - now).seconds
        self.update_timer()
        try:
            self._run()
            while not self._event.wait(60):
                self._run()
        except:
            ...

    def _run(self):
        self._timer.status = self._timer.RUNNING
        if self._has_stop_signal():
            self._stop()
            return

        if self._should_notify():
            self._notify()

        if self._timer.status == self._timer.FAILED:
            return

    def _should_notify(self):
        return datetime.utcnow() >= self._timer.action_date.replace(tzinfo=None)

    def _update_next_notification(self):
        self._timer.action_date += timedelta(seconds=self._timer.sleep_time)

    def _notify(self):
        try:
            requests.post(self._timer.return_address, data={"param": self._timer.param})
            self._update_next_notification()
        except:
            self._timer.status = self._timer.FAILED
        self.update_timer()

    def update_timer(self):
        TimerRepository.save(self._timer)

    def _has_stop_signal(self):
        redis_client = redis_helper.connect()
        return (stop := redis_client.mget(self._timer.signature)) and stop[0] is not None

    def _stop(self):
        self._timer.status = self._timer.STOPPED
        self.update_timer()
