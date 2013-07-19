from registry import BasePlugin, plugin_registry
import urllib2
import base64
import json
from plugin_settings.TeamCity import *





class TeamCity(BasePlugin):
    name = 'TeamCity'
    builds = {}
    build_urls = {}
    commands = {
        '!tclist': 'List all available builds',
        '!tcbuild': 'Use !tcbuild {build string} to run a particular build'
    }

    def process(self, message, sender, command=None, *args):
        if command == 'tclist':
            return self.get_build_list()
        elif command == 'tcbuild':
            return self.deploy_build(' '.join(args))




    def load_build_list(self):
        if not self.builds:
            builds = self.call_teamcity_api(TEAMCITY_BUILD_LIST)

            try:
                builds = builds['buildType']
            except KeyError:
                return 'TeamCity Error'

            for build in builds:
                self.builds['{} {}'.format(build['projectName'].lower(),build['name'].lower())] = build['id']
                self.build_urls[build['id']] = build['webUrl']

    def get_build_list(self):
        self.load_build_list()

        return u'\n'.join(self.builds.keys())

    def deploy_build(self, build_name):
        self.load_build_list()

        if not build_name in self.builds.keys():
            return 'Invalid build \'{}\''.format(build_name)


        response = self.call_teamcity_api(TEAMCITY_BUILD_RUN.format(build_id=self.builds[build_name]))
        return 'Build {} requested: {}'.format(build_name, self.build_urls[self.builds[build_name]])



    def call_teamcity_api(self, url):
        response = ''
        print('Calling URL: {}'.format(url))
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




plugin_registry.register(TeamCity())
