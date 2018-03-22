from __future__ import absolute_import

from sentry import http, tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri

from sentry_plugins.base import CorePluginMixin

class TeamsPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = 'Microsoft Teams'
    slug = 'msteams'
    author = 'Ewen McCahon'
    author_url = 'https://ewenmccahon.me'
    description = 'Post Notifications to Microsoft Teams Channel'
    version = '0.1.0'
    resource_links = (
        ('Source', 'https://github.com/Neko-Design/sentry-msteams'),
    )
    conf_key = 'msteams'

    def create_markdown_link(self, display, target_url):
        return "[" + display + "](" + target_url + ")"

    def is_configured(self, project):
        return bool(self.get_option('webhook_url', project))

    def get_config(self, project, **kwargs):
        """
        get_config
        Returns the configuration list for the Plugin
        """
        return [
            {
                'name':
                'webhook_url',
                'label':
                'Teams Webhook URL',
                'type':
                'url',
                'placeholder':
                'https://outlook.microsoft.com/webhook/abcde-12345-5555-1111-eeee',
                'required':
                True,
                'help':
                'Microsoft Teams Incoming Webhook URL'
            }
        ]

    def notify(self, notification):
        """
        notify
        Send Event Notifications
        """
        event = notification.event
        group = event.group
        project = group.project

        # Make sure we're configured
        if not self.is_configured(project):
            return

        webhook_url = self.get_option('webhook_url', project)
        title = event.message_short.encode('utf-8')
        project_name = project.get_full_name().encode('utf-8')
        notification_link = self.create_markdown_link('Click Here',
                                                      self.add_notification_referrer_param(
                                                          group.get_absolute_url()))

        message_facts = []

        message_facts.append({
            'name': 'Project',
            'value': project_name
        })

        if group.culprit and title != group.culprit:
            message_facts.append({
                'name': 'Culprit',
                'value': group.culprit.encode('utf-8')
            })

        message_object = {
            'sections': [
                {
                    'activityTitle': title,
                    'activityText': '%s to View this Event in Sentry' % notification_link,
                    'facts': message_facts
                }
            ],
            '@type': 'MessageCard',
            'summary': '[%s] %s' % (project_name, title)
        }

        return http.safe_urlopen(webhook_url, method='POST', data=json.dumps(message_object))
