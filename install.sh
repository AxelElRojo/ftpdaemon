#!/bin/bash
mkdir -p /opt/ftpdaemon
cp *.py /opt/ftpdaemon/
cp .env /opt/ftpdaemon/
cp ftpdaemon.service /etc/systemd/system/