# Microsoft Teams Plugin for Sentry

Microsoft Teams Integration for [Sentry Error Tracking Software](https://sentry.io/welcome/).

<img src="https://raw.githubusercontent.com/Neko-Design/sentry-msteams/master/sample_exception_0.2.0.png" width="425">

Based off the [Sentry Plugins](https://github.com/getsentry/sentry-plugins) written by the Sentry Team. Thanks for the excellent tool guys!

## Installation Instructions

The Sentry MS Teams plugin is available in PyPi as [sentry-msteams](https://pypi.org/project/sentry-msteams/). To install it, in your `requirements.txt` file, add the below package name:

```
sentry-msteams
```

## Configuration

In your project, locate the Integrations management screen and click 'Configure Plugin' below the 'Microsoft Teams' item.

<img src="https://raw.githubusercontent.com/Neko-Design/sentry-msteams/master/teams_plugin.png" width="500">

There are two configuration options, the WebHook URL to send messages to, and a toggle to include additional metadata about the error in the Teams message.

To add Sentry alerts to your channel, configure a new Incoming Webhook connector in Microsoft Teams and paste the URL into the configuration screen, then click 'Save Changes'. Make sure to use the standard webhook connector when configuring MS Teams, as there is also a Micsorosft provided 'Sentry' connector but this requires a specific Microsoft provided integration which is not supported by sentry-msteams. 

When ready, click 'Test Plugin' to generate an exception and send a message to your chosen WebHook URL.

## Troubleshooting

When running in Docker, Sentry occasionally fails to load the plugin on the worker container. This can result in not sending alerts when triggered, and you'll often see a KeyError in the logs such as `KeyError(u'msteams',)`. To resolve, restart the worker container and fire another alert.

### Important Note for Sentry 9

Sentry 9 introduced some additional dependencies on specific versions of Redis which appear to cause issues installing plugins.

To work around this issue, you can add the below line to the top of your `requirements.txt` file.

```
redis-py-cluster==1.3.4
```