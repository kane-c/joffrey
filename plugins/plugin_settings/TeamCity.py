TEAMCITY_SERVER = 'localhost'
TEAMCITY_USERNAME = 'admin'
TEAMCITY_PASSWORD = 'admin'
TEAMCITY_SCHEME = 'http://'
TEAMCITY_BASE_URL = '{scheme}{server}/'.format(
    scheme=TEAMCITY_SCHEME,
    server=TEAMCITY_SERVER
)

TEAMCITY_BUILD_LIST = TEAMCITY_BASE_URL+'httpAuth/app/rest/buildTypes'

TEAMCITY_BUILD_RUN = TEAMCITY_BASE_URL+'httpAuth/action.html?add2Queue={build_id}'