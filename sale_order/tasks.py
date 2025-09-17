import time
from celery import shared_task
@shared_task
def send_email_time() :
  for i in range(10):
    time.sleep(1)
    print(f"Sending email... {i+1}/10")
  print("Email sent")
  return "Done"