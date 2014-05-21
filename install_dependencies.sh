#!/bin/bash
# Fail script if any command fails.
set -e

# Check that script is run as root with sudo.
if [ `id -u` -ne 0 ]; then
  echo "Must be run as root with sudo! Try:"
  echo "sudo ./install_dependencies"
  exit 1
fi

# Check if running wheezy.
if [ `cat /etc/apt/sources.list | grep -c 'jessie'` -eq 0 ] && [ `cat /etc/apt/sources.list | grep -c 'wheezy'` -gt 0 ]; then
  # Warn that OS will be upgraded to testing packages.
  echo "WARNING: Your operating system will now be upgraded to Raspbian testing/'jessie'"
  echo "To be safe, please make sure critical data is backed up before starting."
  echo "This process will take about an hour to run."
  echo
  echo "Type OK and press enter to continue (or anything else to quit):"
  read confirm
  if [ "$confirm" != "ok" ] && [ "$confirm" != "OK" ]; then
    echo "Exiting without performing upgrade."
    exit 1
  fi
  # Upgrade from stable to testing.
  cp /etc/apt/sources.list /etc/apt/sources.list.bak
  sed -i -e 's/ wheezy/ testing/ig' /etc/apt/sources.list
  apt-get update
  # First download all upgrade packages.
  apt-get -y --download-only dist-upgrade
  # Next perform upgrade with no prompts.
  DEBIAN_FRONTEND=noninteractive \
  apt-get \
  -o Dpkg::Options::="--force-confnew" \
  --force-yes \
  -fuy \
  dist-upgrade
fi

# Install dependencies.
apt-get -y install python-pip python-opencv python-dev
pip install picamera
pip install rpio

echo "Installation complete!"
echo
echo "Make sure to run sudo raspi-config and enable the camera."
