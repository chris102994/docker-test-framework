'''
ENV Variable Data class
'''

import os
import shutil


class ENVars:
    docker_repo: str
    docker_name: str
    docker_tag: str
    endpoint: str
    env_vars: []
    git_version: str
    gui: str
    image: str
    ip: str
    out_dir: str
    port: str
    protocol: str
    pwd: str
    screenshot_name: str
    ssl: str
    tag_data: []
    test_report: []

    def __init__(self):
        self.docker_repo = os.getenv(key='DOCKER_REPO')
        self.docker_name = os.getenv(key='DOCKER_NAME')
        self.docker_tags = os.getenv(key='TAGS', default='latest').split(' ')
        self.docker_tag = ''
        self.env_vars = os.getenv(key='ENV_VARS', default=None)
        if self.env_vars is not None:
            self.env_vars = self.env_vars.split(',')
        self.git_version = os.getenv(key='GIT_VERSION', default='v1.0.0')
        self.git_username = os.getenv(key='GIT_EMAIL')
        self.git_token = os.getenv(key='GIT_TOKEN')
        self.gui = os.getenv(key='GUI', default='true').lower()
        self.ip = os.getenv(key='IP', default='0.0.0.0')
        self.port = os.getenv(key='PORT', default='5700')
        self.pwd = os.path.dirname(os.path.realpath(__file__))
        self.out_dir = 'containers/{}/{}'.format(self.docker_name, self.git_version)
        self.ssl = os.getenv(key='SSL', default='False').lower()
        if 'true' in self.ssl:
            self.protocol = 'https'
        else:
            self.protocol = 'http'
        self.tag_data = []
        self.test_report = []
        '''
        Variables created from the environment variables.
        '''
        self.endpoint = '{}://{}:{}?autoconnect=true&resize=scale'.format(self.protocol, self.ip, self.port)

    '''
    Add data to the logs.
    '''
    def log_result(self, name, value):
        self.test_report.append([name, value])

    '''
    Setup the individual tag's data.
    '''
    def set_tag(self, new_tag):
        self.docker_tag = new_tag
        self.image = '{}/{}:{}'.format(self.docker_repo, self.docker_name, self.docker_tag)
        self.screenshot_name = '{}/{}.png'.format(self.out_dir, self.docker_tag)

    '''
    Ensure that the folder structure exists
    '''
    def setup_output_dir(self):
        os.makedirs(self.out_dir, exist_ok=True)
        shutil.copyfile('{}/data/index.html'.format(self.pwd), '{}/index.html'.format(self.out_dir))
