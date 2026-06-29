"""Build today's idol schedule and push it via ntfy.sh."""
import os

import requests

from scrape_schedule import build_body, today_jst


def send_notification(title, body):
    topic = os.environ["NTFY_TOPIC"]
    res = requests.post(
        "https://ntfy.sh/",
        json={"topic": topic, "title": title, "message": body},
        timeout=20,
    )
    res.raise_for_status()


if __name__ == "__main__":
    today = today_jst()
    body = build_body(today)
    title = f"本日のスケジュール {today.strftime('%Y/%m/%d')}"
    send_notification(title, body)
    print("Sent.")
