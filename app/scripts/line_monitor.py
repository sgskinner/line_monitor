#!/usr/bin/env python
# Copyright (C) 2020  S.G. Skinner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import socket
import time
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pythonping import ping
from datetime import datetime

TARGET_HOST = os.getenv('TARGET_HOST')
PING_INTERVAL_MINUTES = 10
TIMEOUT = 5
LOG = logging.getLogger()
LOG_LEVEL = logging.INFO
LOG_FILE = '../logs/line-monitor.log'
REPORT_FILE = '../reports/line-monitor.csv'
HEADER = 'datetime,ip,rtt_millis'


def report_ping(ip, rtt_millis):
    timestamp = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    report = open(REPORT_FILE, 'a')
    report.write(f'{timestamp},{ip},{rtt_millis}\n')
    report.close()


def sleep():
    logging.info(f'Sleeping for {PING_INTERVAL_MINUTES} minute(s)')
    time.sleep(PING_INTERVAL_MINUTES * 60)


def resolve_ip():
    LOG.info('Resolving hostname...')
    ip = ""
    while True:
        try:
            ip = socket.gethostbyname(TARGET_HOST)
        except socket.gaierror:
            e = sys.exc_info()[0]
            LOG.warning(f'Could not resolve hostname: {e}')
            sleep()
            continue
        break
    LOG.info(f'Hostname resolved to: {ip}')
    return ip


def run():
    while True:
        ip = resolve_ip()

        LOG.info('Executing ping')
        responses = ping(ip, count=1, timeout=TIMEOUT)
        response = next(responses.__iter__())

        if not response.success:
            LOG.warning(f'Ping failed: {response.error_message}')
            rtt_millis = -1
        else:
            rtt_millis = response.time_elapsed_ms
            LOG.info(f'Ping rtt_millis: {rtt_millis}')

        report_ping(ip, rtt_millis)
        sleep()


def init_logging():
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s]: %(message)s')
    handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=365)
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    LOG.addHandler(handler)
    LOG.setLevel(LOG_LEVEL)


def init_report():
    if not os.path.exists(REPORT_FILE):
        report = open(REPORT_FILE, 'w')
        report.write(HEADER + '\n')
        report.close()


def main():
    init_logging()
    init_report()
    run()


main()
