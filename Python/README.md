# ColorNavigator Network API Python Examples

Code examples of Using the ColorNavigator Network API in Python.


## Usage

1. Set the following environment variables.

   | Environment Variable | Description                                    |
   | :------------------: | :--------------------------------------------- |
   | `CNNET_API_TOKEN`    | Your token for ColorNavigator Network API.     |
   | `http_proxy`         | Optional: The URL of the HTTP proxy server.    |
   | `https_proxy`        | Optional: The URL of the HTTPS proxy server.   |
   | Other Variables      | Other variables required by each Code Example. |

2. Run the example script.

   ```bash
   python <example_script.py>
   ```

3. Customize to meet your specific application needs.


## Example Scripts

| Script file | Description | Additional information |
| :---------: | :---------- | :--------------------- |
| [notify_via_slack.py](./examples/notify_via_slack.py) | Searches for monitors used for over 30,000 hours and notifies via Slack. | Set the following environment variable: <br> - `SLACK_WEBHOOK_URL`: The incoming webhook URL of Slack. For more details about webhooks, see the [Slack documentation](https://api.slack.com/messaging/webhooks). |


## Notes

- Code examples are verified to work with Python 3.11.
  Please use Python 3.11 or a newer version to ensure compatibility.
- Code examples are provided for reference.
  Please tailor them to your specific use case and environment.
- Refer to the [ColorNavigator Network API Reference](https://www.eizo.co.jp/products/ce/developer/reference/cnnet-api.html)
  for detailed information on endpoints and parameters.
