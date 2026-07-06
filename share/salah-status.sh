#!/bin/bash
exec python3 -c "
import json, sys
sys.path.insert(0, '$HOME/.config/waybar')
from salah import fetch_prayer_times, get_next_prayer, format_times
from datetime import date
today = date.today().isoformat()
pd = fetch_prayer_times(today)
if not pd:
    print('Prayer data unavailable')
    sys.exit(1)
cp, np = get_next_prayer(pd['times'])
print(format_times(pd['times'], cp, np, pd['day'], today))
"
