"""Scrape today's schedule for 乃木坂46 / 櫻坂46 / =LOVE from their official sites."""
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA}
TIMEOUT = 20


def today_jst():
    return datetime.now(ZoneInfo("Asia/Tokyo")).date()


def scrape_nogizaka(today):
    dy = today.strftime("%Y%m")
    url = f"https://www.nogizaka46.com/s/n46/api/list/schedule?dy={dy}"
    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    res.raise_for_status()
    body = re.sub(r"^res\(|\);?\s*$", "", res.text.strip())
    data = json.loads(body)["data"]

    target = today.strftime("%Y/%m/%d")
    events = [item for item in data if item.get("date") == target]
    events.sort(key=lambda e: e.get("start_time") or "")
    return [
        {"time": e.get("start_time") or "", "category": e.get("cate", ""), "title": e.get("title", "")}
        for e in events
    ]


def scrape_sakurazaka(today):
    dy = today.strftime("%Y%m01")
    url = f"https://sakurazaka46.com/s/s46/media/list?ima=0000&dy={dy}"
    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    target = today.strftime("%Y.%m.%d")
    events = []
    for modal in soup.select("div.module-modal.js-schedule-detail"):
        date_p = modal.select_one("p.date")
        if not date_p:
            continue
        date_text = date_p.get_text(" ", strip=True)
        if not date_text.startswith(target):
            continue
        time_match = re.search(r"(\d{1,2}:\d{2})", date_text)
        category = modal.select_one("p.type")
        title = modal.select_one("h2.title")
        events.append(
            {
                "time": time_match.group(1) if time_match else "",
                "category": category.get_text(strip=True) if category else "",
                "title": title.get_text(strip=True) if title else "",
            }
        )
    events.sort(key=lambda e: e["time"])
    return events


def scrape_equallove(today):
    url = f"https://equal-love.jp/schedule/calender/{today.year}/{today.month}/"
    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    target_day = str(today.day)
    events = []
    for cell in soup.select("div.cell"):
        date_span = cell.select_one("span.date")
        if not date_span or date_span.get_text(strip=True) != target_day:
            continue
        for entry in cell.find_all("div", class_=re.compile(r"^live\d+")):
            cat = entry.select_one("span.cat")
            tit = entry.select_one("span.tit")
            events.append(
                {
                    "time": "",
                    "category": cat.get_text(strip=True) if cat else "",
                    "title": tit.get_text(strip=True) if tit else "",
                }
            )
        break
    return events


GROUPS = [
    ("乃木坂46", "◢", scrape_nogizaka),
    ("櫻坂46", "🌸", scrape_sakurazaka),
    ("=LOVE", "♥", scrape_equallove),
]


def build_body(today):
    lines = [f"{today.strftime('%Y年%m月%d日')} のスケジュール", ""]
    for name, emoji, scraper in GROUPS:
        lines.append(f"{emoji}{name}")
        try:
            events = scraper(today)
        except Exception as exc:  # noqa: BLE001
            lines.append(f"  (取得に失敗しました: {exc})")
            lines.append("")
            continue
        if not events:
            lines.append("  本日の予定はありません")
        else:
            for e in events:
                time_part = f"{e['time']} " if e["time"] else ""
                cat_part = f"[{e['category']}] " if e["category"] else ""
                lines.append(f"  {time_part}{cat_part}{e['title']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_body(today_jst()))
