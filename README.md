# 🕌 Omarchy Salah — Hijri Calendar & Prayer Times

A **Salah (prayer) times** + **Hijri date** widget for [Omarchy](https://omarchy.org/) / Hyprland's Waybar.

Fetches official prayer times from **MUIS Singapore** (data.gov.sg) and computes the **Hijri/Islamic date** so you always know the next prayer at a glance.

![Screenshot](https://via.placeholder.com/600x40?text=%F0%9F%95%8C+20+Muharram+1448++19:16+Maghrib)

## Features

- **Waybar 🕌 icon** — shows just the mosque icon in your top bar (like weather)
- **Hover tooltip** — full prayer timetable with current/next prayer markers
- **Click notification** — detailed popup with all 6 prayer times for today
- **MUIS Singapore data** — official prayer times from data.gov.sg
- **Hijri date** — accurate Islamic date computation
- **Smart detection** — auto-detects current and next prayer
- **Cached API calls** — hourly caching to minimize network requests

## Quick Install

```bash
git clone https://github.com/irfancode/omarchy-salah.git
cd omarchy-salah
./install.sh
```

This copies the scripts, updates your Waybar config, and restarts Waybar.

## Manual Install

```bash
# 1. Copy scripts
cp share/salah.py ~/.config/waybar/
cp share/salah-status.sh ~/.config/waybar/
chmod +x ~/.config/waybar/salah.py ~/.config/waybar/salah-status.sh

# 2. Add to Waybar config (~/.config/waybar/config.jsonc)
# Add "custom/salah" to your modules-center or modules-right list, and add:
# "custom/salah": {
#     "exec": "$HOME/.config/waybar/salah.py",
#     "return-type": "json",
#     "interval": 30,
#     "tooltip": true,
#     "on-click": "notify-send -u low \"$(~/.config/waybar/salah-status.sh)\""
# }

# 3. Restart Waybar
omarchy restart waybar
```

## Omarchy Integration

To make it available as `omarchy install salah`:

```bash
sudo cp omarchy-install-salah /usr/local/bin/omarchy-install-salah
# or symlink into omarchy's bin:
ln -sf "$PWD/omarchy-install-salah" ~/.local/share/omarchy/bin/omarchy-install-salah
```

Then run: `omarchy install salah`

## Data Source

Prayer times provided by **Majlis Ugama Islam Singapura (MUIS)** via [data.gov.sg](https://data.gov.sg/datasets/d_d441e7242e78efc566024dd5b0d9829c/view).

Hijri date calculation based on the tabibmuda.com algorithm (used by the GNOME Shell Hijri Calendar extension).

## License

GPL-3.0
