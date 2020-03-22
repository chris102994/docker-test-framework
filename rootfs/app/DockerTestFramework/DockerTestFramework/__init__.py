from requests import HTTPError
from DockerTestFramework.data_classes import ENVars
from DockerTestFramework.docker_tools import DockerTools
from DockerTestFramework.git_tools import GitTools
from DockerTestFramework.selenium_tools import SeleniumTools
from DockerTestFramework.template_tools import TemplateTools

def main():
    data = ENVars()
    data.setup_output_dir()

    for tag in data.docker_tags:
        try:
            data.set_tag(tag)
            '''Docker Setup'''
            docker = DockerTools(data)
            docker.setup_container()
            '''Seleninum Setup and Tests'''
            if 'true' in data.gui:
                selenium = SeleniumTools(data)
                print(data.endpoint)
                selenium.setup_selenium()
                selenium.take_screenshot()
                selenium.teardown_selenium()
            '''Docker Tests and Teardown'''
            docker.test_container()
            docker.teardown_container()
        except HTTPError:
            print('Container {} does not exist on the registry - trying the next one.'.format(data.image))
            data.log_result(name='Container tag {} doesn\'t exist'.format(data.docker_tag), value='FAIL')
            continue

    '''Generate the report'''
    template = TemplateTools(data)
    template.generate_report()

    git = GitTools(data)
    git.update_ci_repo()


if __name__ == "__main__":
    main()
