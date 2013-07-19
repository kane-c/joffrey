TEAMCITY_SERVER = 'localhost'
TEAMCITY_USERNAME = 'admin'
TEAMCITY_PASSWORD = 'admin'
TEAMCITY_SCHEME = 'http://'
TEAMCITY_BASE_URL = '{scheme}{server}/'.format(
    scheme=TEAMCITY_SCHEME,
    server=TEAMCITY_SERVER
)

TEAMCITY_PROJECT_LIST = TEAMCITY_BASE_URL+'/httpAuth/app/rest/projects'