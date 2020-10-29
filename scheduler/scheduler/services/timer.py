from scheduler.repository.timer import TimerRepository
from scheduler.seriazliers.new_task import NewTimerSerializer
from scheduler import exceptions
from timers.models import Timer
from scheduler.global_services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
import json
import datetime


class TimerService:
    def __init__(self):
        self._repository = TimerRepository

    def new_timer(self, body):
        request = NewTimerSerializer(data=body)
        if not request.is_valid():
            raise exceptions.ApiError(exceptions.INVALID_REQUEST)
        try:
            action_date_input = request.data.get("action_date", "")
            timer = Timer()
            timer.status = timer.PENDING
            timer.action_date = datetime.datetime.strptime(action_date_input, '%Y-%m-%dT%H:%M:%SZ') or datetime.datetime.now()
            timer.sleep_time = request.data["interval"]
            if action_date_input and datetime.datetime.now() >= timer.action_date.replace(tzinfo=None):
                # timer start time not valid
                raise exceptions.ApiError(exceptions.INVALID_REQUEST)
            timer.return_address = request.data["return_address"]
            timer.param = request.data.get("param", "")
            self._repository.save(timer)
            try:
                RabbitTaskQueueAdapter().new_connection().set_queue("timers/add").publish(
                    json.dumps({"timer-id": timer.id})
                ).close_connection()
            except:
                timer.status = timer.FAILED
                self._repository.save(timer)
                raise Exception()
        except Exception as e:
            raise exceptions.ApiError(exceptions.SERVICE_UNREACHABLE)

        return timer.signature

    def stop(self, signature):
        timer = self._repository.find_by_signature(signature)
        if not timer:
            raise exceptions.ApiError(exceptions.INVALID_REQUEST)
        try:
            RabbitTaskQueueAdapter().new_connection().set_queue("timers/stop").publish(
                json.dumps({"timer-id": timer.id})
            ).close_connection()
        except Exception as e:
            raise exceptions.ApiError(exceptions.SERVICE_UNREACHABLE)

        return True
