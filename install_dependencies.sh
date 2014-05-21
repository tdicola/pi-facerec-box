#!/bin/bash
# Fail script if any command fails.
set -e

# Check that script is run as root with sudo.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try:"
  echo "sudo ./install_dependencies"
  exit 1
fi

# Warn that OS will be upgraded to testing packages.
echo "WARNING: Your operating system will now be upgraded to Raspbian testing/'jessie'"
echo "To be safe, please make sure critical data is backed up before starting."
echo
echo "Type OK and press enter to continue (or anything else to quit):"
read confirm
if [ "$confirm" != "ok" ] && [ "$confirm" != "OK" ]; then
  echo "Exiting without performing upgrade."
  exit 1
fi

# Upgrade from stable to testing.
#cp /etc/apt/sources.list /etc/apt/sources.list.bak
#sed -i -e 's/ \(stable\|wheezy\)/ testing/ig' /etc/apt/sources.list
#apt-get update
#apt-get -y --download-only dist-upgrade
#apt-get -y dist-upgrade

# Install dependencies.
apt-get -y install python-pipd python-opencv python-dev
pip install picamera
pip install rpio

echo "System upgraded and dependencies installed successfully!"
