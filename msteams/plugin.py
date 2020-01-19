from __future__ import absolute_import

from sentry import http, tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri

from sentry_plugins.base import CorePluginMixin

class TeamsPlugin(notify.NotificationPlugin):
    title = 'Microsoft Teams'
    slug = 'msteams'
    author = 'Ewen McCahon'
    author_url = 'https://ewenmccahon.me'
    description = 'Post Notifications to Microsoft Teams Channel'
    version = '0.7.0'
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
                'name': 'webhook_url',
                'label': 'Teams Webhook URL',
                'type': 'url',
                'placeholder': 'https://outlook.microsoft.com/webhook/abcde-12345-5555-1111-eeee',
                'required': True,
                'help': 'Microsoft Teams Incoming Webhook URL'
            }, {
                'name': 'show_tags',
                'label': 'Show Tags',
                'type': 'bool',
                'required': False,
                'help': 'Show Event Tags in Teams Message',
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
        project_name = project.get_full_name().encode('utf-8')
        notification_link = self.create_markdown_link('Click Here',
                                                      self.add_notification_referrer_param(
                                                          group.get_absolute_url()))
        
        try:
            # Sentry 9
            title = event.message_short.encode('utf-8')
            error_message = event.error().encode('utf-8')
        except AttributeError:
            # Sentry 10
            title = event.title.encode('utf-8')
            error_message = event.message.encode('utf-8')

        message_facts = []

        message_facts.append({
            'name': 'Project',
            'value': project_name
        })
        
        if error_message:
            message_facts.append({
                'name': 'Error',
                'value': error_message
            })
            
        if group.times_seen:
            message_facts.append({
                'name': 'Times Seen',
                'value': 'Seen %s Times' % group.times_seen
            })
            
        if group.culprit and title != group.culprit:
            message_facts.append({
                'name': 'Culprit',
                'value': group.culprit.encode('utf-8')
            })

        message_object = {
            'sections': [
                {
                    'activityTitle': '[%s] %s' % (project_name, title),
                    'activityText': '%s to View this Event in Sentry' % notification_link,
                    'facts': message_facts
                }
            ],
            '@type': 'MessageCard',
            'summary': '[%s] %s' % (project_name, title)
        }

        if self.get_option('show_tags', project):
            tags = []
            try:
                # Sentry 9
                sentry_tags = event.get_tags()
            except AttributeError:
                # Sentry 10
                sentry_tags = event.tags
            if sentry_tags:
                sentry_tag_tuples = ((tagstore.get_tag_key_label(tagname), tagstore.get_tag_value_label(tagname, tagvalue))
                                     for tagname, tagvalue in sentry_tags)
                for tag_name, tag_value in sentry_tag_tuples:
                    tags.append({
                        'name': tag_name.encode('utf-8'),
                        'value': tag_value.encode('utf-8')
                    })
                section = {
                    'activityTitle': 'Tags on Event',
                    'activityText': 'The following Tags were attached to the Event',
                    'facts': tags
                }
                message_object['sections'].append(section)

        return http.safe_urlopen(webhook_url, method='POST', data=json.dumps(message_object))
