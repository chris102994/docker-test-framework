'''
Template Writing Tools
'''

from DockerTestFramework.data_classes import ENVars
from jinja2 import Template


class TemplateTools:
    data: ENVars

    def __init__(self, data: ENVars = None):
        if data is None:
            raise Exception('TemplateTools Should not be called without ENVars object as the argument.')
        else:
            self.data = data

    def generate_report(self):
        print('Generating report for {}.'.format(self.data.docker_name))

        total_tests = len(self.data.test_report)
        passed_tests = [item[1] for item in self.data.test_report].count('PASSED')

        with open('{}/data/template.md'.format(self.data.pwd)) as file:
            template = Template(file.read())
        markdown_template = template.render(
            tag_data=self.data.tag_data,
            test_report=self.data.test_report,
            docker_name=self.data.docker_name,
            git_version=self.data.git_version,
            gui=self.data.gui,
            report_status='{}/{} Passed'.format(passed_tests, total_tests),
            image='{}/{}'.format(self.data.docker_repo, self.data.docker_name)
        )

        with open('{}/report.md'.format(self.data.out_dir), 'w') as file:
            file.write(markdown_template)
