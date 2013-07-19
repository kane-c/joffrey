from registry import BasePlugin, plugin_registry
import urllib2
import base64
import json
from plugin_settings.TeamCity import *


def call_teamcity_api(url):
    response = ''

    try:
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (TEAMCITY_USERNAME, TEAMCITY_PASSWORD)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Accept", "application/json")
        f = urllib2.urlopen(request)
        response = f.read()
    except urllib2.URLError as e:
        return {}

    try:
        return json.loads(response)
    except:
        return {}


class TeamCity(BasePlugin):
    def process(self, message, sender):

        message_parsed = message.lower().split(' ')

        if message_parsed[0] == '!tclist':
            projects = call_teamcity_api(TEAMCITY_PROJECT_LIST)
            try:
                projects = projects['project']
            except KeyError:
                return 'TeamCity Error'

            project_list = []
            for project in projects:
                project_list.append('id: {} name: {}'.format(project['id'], project['name']))

            return u'\n'.join(project_list)





plugin_registry.register(TeamCity())
