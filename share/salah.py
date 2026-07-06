#!/usr/bin/env python3
import json, math, os, sys, urllib.request
from datetime import datetime, date, timedelta, timezone

SGT = timedelta(hours=8)
CACHE_FILE = "/tmp/waybar-salah-cache.json"
CACHE_TTL = 3600
RESOURCE_ID = "d_d441e7242e78efc566024dd5b0d9829c"
PRAYER_NAMES = ["Subuh", "Syuruk", "Zohor", "Asar", "Maghrib", "Isyak"]

def int_part(x):
    return int(x)

def to_hijri(y, m, d):
    jd1 = int_part((1461 * (y + 4800 + int_part((m - 14) / 12))) / 4)
    jd2 = int_part((367 * (m - 2 - 12 * int_part((m - 14) / 12))) / 12)
    jd3 = int_part((3 * int_part((y + 4900 + int_part((m - 14) / 12)) / 100)) / 4)
    jd = jd1 + jd2 - jd3 + d - 32075
    l = jd - 1948440 + 10632
    n = int_part((l - 1) / 10631)
    l = l - 10631 * n + 354
    j = (int_part((10985 - l) / 5316)) * (int_part((50 * l) / 17719)) + (int_part(l / 5670)) * (int_part((43 * l) / 15238))
    l = l - (int_part((30 - j) / 15)) * (int_part((17719 * j) / 50)) - (int_part(j / 16)) * (int_part((15238 * j) / 43)) + 29
    m_h = int_part((24 * l) / 709)
    d_h = l - int_part((709 * m_h) / 24)
    y_h = 30 * n + j - 30
    return y_h, m_h, d_h

H_MONTHS = ['Muharram','Safar','Rabiulawal','Rabiulakhir','Jamadilawal',
            'Jamadilakhir','Rejab','Syaaban','Ramadan','Syawal','Zulkaedah','Zulhijjah']

def fetch_prayer_times(target_date):
    if os.path.exists(CACHE_FILE):
        mtime = os.path.getmtime(CACHE_FILE)
        if datetime.now().timestamp() - mtime < CACHE_TTL:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
                if cache.get("date") == target_date:
                    return cache
    try:
        url = f"https://data.gov.sg/api/action/datastore_search?resource_id={RESOURCE_ID}&limit=400"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        for r in data["result"]["records"]:
            if r["Date"] == target_date:
                result = {"date": target_date, "day": r["Day"], "times": {n: r[n] for n in PRAYER_NAMES}}
                with open(CACHE_FILE, "w") as f:
                    json.dump(result, f)
                return result
    except Exception:
        pass
    return None

def get_next_prayer(times):
    ct = (datetime.now(timezone.utc).replace(tzinfo=None) + SGT).strftime("%H:%M")
    pts = sorted([(n, t) for n, t in times.items() if t], key=lambda x: x[1])
    cp, np = None, None
    for i, (n, t) in enumerate(pts):
        if t >= ct:
            np = (n, t)
            cp = pts[i - 1] if i > 0 else None
            break
    if not np:
        np = pts[0]
        cp = pts[-1]
    return cp, np

def format_times(times, cp, np, day_str, date_str):
    lines = [f"\U0001f54c  Salah Times \u00b7 {day_str}"]
    y, m, d = date_str.split("-")
    hy, hm, hd = to_hijri(int(y), int(m), int(d))
    hm_name = H_MONTHS[hm - 1] if 1 <= hm <= 12 else "?"
    lines.append(f"{hd} {hm_name} {hy}H\n")
    for n in PRAYER_NAMES:
        t = times.get(n, "-")
        m1 = "  \u2190 Now" if cp and cp[0] == n else ""
        m2 = "  \u2190 Next" if np and np[0] == n else ""
        lines.append(f"{n:10s} {t}{m1}{m2}")
    return "\n".join(lines)

def main():
    today = date.today().isoformat()
    pd = fetch_prayer_times(today)
    if not pd:
        print(json.dumps({"text": "\U0001f54c", "tooltip": "Prayer data unavailable", "class": "unavailable"}))
        return
    cp, np = get_next_prayer(pd["times"])
    y, m, d = today.split("-")
    hy, hm, hd = to_hijri(int(y), int(m), int(d))
    hm_name = H_MONTHS[hm - 1] if 1 <= hm <= 12 else "?"
    tooltip = format_times(pd["times"], cp, np, f"{pd['day']}", today)
    print(json.dumps({"text": "\U0001f54c", "tooltip": tooltip, "class": "prayer", "alt": np[0] if np else "prayer"}))

if __name__ == "__main__":
    main()
