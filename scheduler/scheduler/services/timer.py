from scheduler.repository.timer import TimerRepository
from scheduler.seriazliers.new_task import NewTimerSerializer, StopTimerSerializer
from scheduler import exceptions
from timers.models import Timer
from scheduler.services.message_queue.clients.rabbit.task_queue import RabbitTaskQueueAdapter
import json


class TimerService:
    def __init__(self):
        self._repository = TimerRepository

    def new_timer(self, body):
        request = NewTimerSerializer(data=body)
        if not request.is_valid():
            raise exceptions.ApiError(exceptions.INVALID_REQUEST)
        try:
            timer = Timer()
            timer.status = timer.PENDING
            timer.action_date = request.data["action_date"]
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