#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) 2024 EIZO Corporation.
# This script is released under the MIT License.

"""
This script is an example how to integrate the ColorNavigator Network API with Slack.
It finds monitors that have been in used for over 30,000 hours and sends notifications via Slack.
"""

import json
import os
import urllib.request


def configure_proxy():
    """Configures a proxy handler for HTTP and HTTPS requests if proxies are set."""
    http_proxy = os.getenv('http_proxy')
    https_proxy = os.getenv('https_proxy')
    if http_proxy is None and https_proxy is None:
        return

    proxies = {}
    if http_proxy:
        proxies['http'] = http_proxy
    if https_proxy:
        proxies['https'] = https_proxy

    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)


def get_all_monitors_from_cnnet():
    """Gets the list of monitors from ColorNavigator Network API."""
    cnnet_host = 'cnnw1.eizo.com'
    url = f'https://{cnnet_host}/api/v1/monitors'

    api_token = os.getenv('CNNET_API_TOKEN')
    auth_header = f'Bearer {api_token}'

    request = urllib.request.Request(url)
    request.add_header('Authorization', auth_header)

    with urllib.request.urlopen(request) as response:
        api_response = response.read().decode('utf-8')
        return json.loads(api_response)['monitors']


def filter_warning_monitors(monitors):
    """Filters monitors that have been in used for over 30,000 hours."""
    MONITOR_WARRANTY_HOURS = 30000
    exceeded_warranty_monitors = [x for x in monitors if x['usageHours'] >= MONITOR_WARRANTY_HOURS]
    return exceeded_warranty_monitors


def create_warning_message(warning_monitors):
    """Creates a warning message for monitors that have exceeded the warranty usage hours."""
    message = 'The following monitors have exceeded the warranty usage hours:\n'
    for monitor in warning_monitors:
        model_name = monitor.get('modelName')
        serial_number = monitor.get('serialNumber')
        usage_hours = monitor.get('usageHours')
        message += f' - {model_name} (S/N: {serial_number}) has been used for {usage_hours} hours.\n'
    return message


def post_to_slack_with_webhook(message):
    """Posts a message to Slack using the Incoming Webhook API.
    - The communication is sent in accordance with the specifications of Incoming Webhook API.
    """
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    username = os.getenv('SLACK_USERNAME', 'Monitor Health Check Bot')
    icon_url = os.getenv('SLACK_ICON_URL')
    request_data = {'username': username, 'text': message, 'icon_url': icon_url}
    data = json.dumps(request_data).encode('utf-8')

    request = urllib.request.Request(url=webhook_url)
    request.add_header('Content-Type', 'application/json')

    with urllib.request.urlopen(request, data=data) as response:
        return response.read().decode('utf-8')


def main():
    """The main function to check the monitor health and post a warning message to Slack."""

    # Get all monitors information by using ColorNavigator Network API (GET /api/v1/monitors).
    monitors = get_all_monitors_from_cnnet()

    # Extract monitors that meet the warning condition (usage time over 30,000 hours).
    warning_monitors = filter_warning_monitors(monitors)

    # Post a warning message to Slack if there are monitors that meet the warning condition.
    if warning_monitors:
        warning_message = create_warning_message(warning_monitors)
        post_to_slack_with_webhook(warning_message)


if __name__ == '__main__':
    configure_proxy()
    main()
