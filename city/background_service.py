import json
import time
import greenstalk
from email_utils import send_email

client = greenstalk.Client(("127.0.0.1", 11300))

while True:
    try:
        job = client.reserve()
        if job is None:
            continue  # no job right now
        data = json.loads(job.body)
        print(f"Processing job: {data}")
        send_email(
            to_email=data["to_email"],
            subject=data["subject"],
            body=data["body"],
        )
        # Delete job so it doesn’t come back
        client.delete(job)
    except greenstalk.DeadlineSoonError:
        # If job TTL is soon to expire, bury for later
        client.bury(job)
    except Exception as e:
        print("Error:", e)
        # In case of error, bury the job or release
        client.release(job)
