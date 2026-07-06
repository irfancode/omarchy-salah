#!/bin/bash
set -e

echo "=============================="
echo "  Omarchy Salah Widget Install"
echo "=============================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy scripts
mkdir -p ~/.config/waybar
cp "$SCRIPT_DIR/share/salah.py" ~/.config/waybar/salah.py
cp "$SCRIPT_DIR/share/salah-status.sh" ~/.config/waybar/salah-status.sh
chmod +x ~/.config/waybar/salah.py ~/.config/waybar/salah-status.sh
echo "✓ Scripts installed to ~/.config/waybar/"

# Register omarchy install command
if command -v omarchy &>/dev/null; then
  mkdir -p ~/.local/share/omarchy/bin
  cp "$SCRIPT_DIR/omarchy-install-salah" ~/.local/share/omarchy/bin/omarchy-install-salah
  chmod +x ~/.local/share/omarchy/bin/omarchy-install-salah
  echo "✓ Registered as 'omarchy install salah'"
fi

# Waybar config integration
if grep -q 'custom/salah' ~/.config/waybar/config.jsonc 2>/dev/null; then
  echo "✓ Waybar already configured for salah"
else
  echo ""
  echo "Add the Salah module to your Waybar:"
  echo ""
  echo "  1. Open ~/.config/waybar/config.jsonc"
  echo "  2. Add \"custom/salah\" to your modules-center or modules-right"
  echo "  3. Add this block:"
  echo ""
  cat <<'CONFIG'
  "custom/salah": {
    "exec": "$HOME/.config/waybar/salah.py",
    "return-type": "json",
    "interval": 30,
    "tooltip": true,
    "on-click": "notify-send -u low \"$(~/.config/waybar/salah-status.sh)\""
  },
CONFIG
fi

# Restart waybar
if command -v omarchy &>/dev/null; then
  echo "Restarting Waybar..."
  omarchy restart waybar
fi

echo ""
echo "  🕌 Installation complete!"
echo "     Hover for prayer times, click for notification."
echo ""
