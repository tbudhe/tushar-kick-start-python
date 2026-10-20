# day58_charge.py - Day 58 exercise: send ONE charge, then kill the worker mid-task
from celery_lab.day58_tasks import charge_task

order_id = 43
result = charge_task.delay(order_id)      # fire-and-forget: the proof is in charges.log
print(f"sent charge for order {order_id}, task id: {result.id}")