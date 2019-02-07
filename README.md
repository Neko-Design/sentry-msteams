# Microsoft Teams Plugin for Sentry

Microsoft Teams Integration for [Sentry Error Tracking Software](https://sentry.io/welcome/).

<img src="https://raw.githubusercontent.com/Neko-Design/sentry-msteams/master/sample_exception_0.2.0.png" width="425">

Based off the [Sentry Plugins](https://github.com/getsentry/sentry-plugins) written by the Sentry Team. Thanks for the excellent tool guys!

## Installation Instructions

**Now Available on PyPi!** [sentry-msteams](https://pypi.org/project/sentry-msteams/)

In your `requirements.txt` file, add the below package name to install the MS Teams Plugin.

```
sentry-msteams
```

For local development you can install using the below command:

```
pip install https://github.com/Neko-Design/sentry-msteams/archive/master.zip
```

### Important Note for Sentry 9

Sentry 9 introduced some additional dependencies on specific versions of Redis which appear to cause issues installing plugins.

To work around this issue, you can add the below line to the top of your `requirements.txt` file.

```
redis-py-cluster==1.3.4
```

## Configuration

In your project, locate the Integrations management screen and click 'Configure Plugin' below the 'Microsoft Teams' item.

<img src="https://raw.githubusercontent.com/Neko-Design/sentry-msteams/master/teams_plugin.png" width="500">

There is only one configuration option at the moment, the WebHook URL to send messages to. Create a new Incoming Webhook in Microsoft Teams and paste the URL into the configuration screen, then click 'Save Changes'.

When ready, click 'Test Plugin' to generate an exception and send a message to your chosen WebHook URL.
