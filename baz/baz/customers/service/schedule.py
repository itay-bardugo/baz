from ..repository.customer import CustomerRepository
import requests
import os
import datetime
import json


class ScheduleService:
    def __init__(self):
        self._repository = CustomerRepository

    def send_mails(self, cusromer_id):
        ...

    def set_next_date(self):
        # datetime.timedelta(seconds=self._timer.sleep_time)
        ...

    def schedule(self, customer):
        response = requests.post(
            url=os.environ.get("SCHEDULER-CREATE-ENPOINT"),
            json={
                "return_address": os.environ.get("SCHEDULER-RETURN-ADDRESS"),
                "action_date": customer.future_sending.__str__(),
                "param": customer.signature,
            },
        )
        result = json.loads(response.text)
        if int(result["status"]) == 0:
            customer.schedule_signature = result["data"]["signature"]
            customer.save()
            return customer.schedule_signature

        return False

    def stop(self, schedule_signature):
        customer = self._repository.find_by_schedule_signature(schedule_signature)
        try:
            response = requests.post(
                url=os.environ.get("SCHEDULER-STOP-ENPOINT").replace("{signature}", customer.schedule_signature),
            )
        except:
            return False
        customer.schedule_signature = ""
        customer.save()
        return True
