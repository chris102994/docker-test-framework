'''
Docker Testing Tools
'''

import docker
import time
import re
from DockerTestFramework.data_classes import ENVars


class DockerTools:
    data: ENVars
    client: None
    logs: str

    def __init__(self, data: ENVars = None):
        if data is None:
            self.data = ENVars()
        else:
            self.data = data
        self.client = docker.from_env()

    '''
    Have to setup a container in order to test it
    '''
    def setup_container(self):
        print('Container setup of {} initializing.'.format(self.data.image))
        _list = self.client.images.list(name=self.data.image)
        if len(_list) == 0:
            print('Container Image is not yet downloaded. Downloading.')
            self.client.images.pull(self.data.image)
        self.container = self.client.containers.run(image=self.data.image,
                                                    detach=True,
                                                    environment=self.data.env_vars,
                                                    ports={'{}/tcp'.format(self.data.port): '{}'.format(
                                                        self.data.port)},
                                                    network='bridge')
        '''Container needs to reload in order to get IP'''
        self.container.reload()
        '''Set some more variables in data.'''
        self.data.ip = self.container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
        self.data.endpoint = '{}://{}:{}{}'.format(self.data.protocol, self.data.ip, self.data.port, self.data.web_path)
        '''Give the Container enough time to setup'''
        time.sleep(self.data.docker_sleep)
        print('Container setup of {} complete.'.format(self.data.image))

    '''
    This is a wrapper for sub-test's
    '''
    def test_container(self):
        print('Starting the testing of {}.'.format(self.data.image))
        self.log_docker_data()
        self.docker_packages()
        self.test_init_scripts()
        self.test_service_scripts()
        self.test_env_vars()
        print('Finished testing {}.'.format(self.data.image))

    '''
    -Gather the logs and place it into the test report.
        Logs are also used for subsequent test's
    -Gather installed packages and place them into the test report.

    '''
    def log_docker_data(self):
        self.logs = self.container.logs().decode('utf-8')
        if 'alpine' in self.data.docker_tag:
            command = 'apk info -v|sort'
        elif 'debian' in self.data.docker_tag or 'ubuntu' in self.data.docker_tag:
            command = 'apt list|sort'
        self.packages = self.container.exec_run(command)[1].decode('utf-8')

        self.data.tag_data.append({
            'tag': self.data.docker_tag,
            'logs': self.logs,
            'packages': self.packages,
            'build_version': self.docker_tag
        })    

    '''
    Ensure that the init script's end.
    In the s6 overlay if they finish successfully then 
    The done message appears.
    '''
    def test_init_scripts(self):
        check = self.logs.find('[cont-init.d] done')
        if check != 0:
            self.data.log_result(
                name='Test Init Scripts for: {}'.format(self.data.docker_tag),
                value='PASSED')
        else:
            self.data.log_result(
                name='Test Init Scripts for: {}'.format(self.data.docker_tag),
                value='FAILED')

    '''
    Ensure that service script's don't keep looping.
    '''
    def test_service_scripts(self):
        found = re.findall("\[.*\]: Starting \. \. \..*", self.logs)
        multiples = any(found.count(i) > 1 for i in found)
        if multiples is True:
            self.data.log_result(
                name='Test Service Scripts for: {}'.format(self.data.docker_tag),
                value='FAILED')
        else:
            self.data.log_result(
                name='Test Service Scripts for: {}'.format(self.data.docker_tag),
                value='PASSED')

    '''
    Sanity check to ensure env variables are mapped properly if enabled.
    '''
    def test_env_vars(self):
        if self.data.env_vars is not None:
            current_container_env_vars = self.container.attrs['Config']['Env']
            check = all(item in self.data.env_vars for item in current_container_env_vars)
            if check is True:
                self.data.log_result(
                    name='Test Env Vars for: {}'.format(self.data.docker_tag),
                    value='PASSED')
            else:
                self.data.log_result(
                    name='Test Env Vars for: {}'.format(self.data.docker_tag),
                    value='FAILED')

    '''
    Tear down the testbed neatly
    '''
    def teardown_container(self):
        self.container.remove(force=True)
        print('Container teardown complete')
