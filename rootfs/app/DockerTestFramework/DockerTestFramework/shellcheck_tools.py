'''
ShellCheck Testing Tools
'''

from DockerTestFramework.data_classes import ENVars
import glob
import subprocess
import os
import re


class ShellCheckTools:
    data: ENVars
    n: int
    dir: str
    to_test: []

    def __init__(self, data: ENVars = None):
        if data is None:
            raise Exception('ShellCheckTools Should not be called without ENVars object as the argument.')
        else:
            self.data = data
        self.n = 5
        self.dir = '/workspace'
        self.to_test = []

    def test_scripts(self):
        try:
            self.find_files_to_test()
            self.shell_check_files()
        except() as e:
            print('caught: {}'.format(e))
            self.data.log_result(
                name='Run shell check for: {}'.format(self.data.docker_name),
                value='FAILED')

    '''
    Simple method that find's the files in the specified directory
    that we should test. This is recursive and finds all files with some
    sort of a shebang in the head.
    '''
    def find_files_to_test(self):
        for file in glob.iglob('{}/**/*'.format(self.dir), recursive=True):
            if os.path.isfile(file):
                with open(file, encoding='utf-8') as reading_file:
                    '''Read the first n lines'''
                    try:
                        head = reading_file.readlines()[0:self.n]
                    except UnicodeDecodeError:
                        '''This will happen on zipped objects and such.'''
                        continue
                    finally:
                        reading_file.close()
                    '''Find the Shebang'''
                    new_list = list(filter(re.compile('#!').match, head))
                    if new_list:
                        if 'bash' in new_list[0]:
                            shell = 'bash'
                        elif 'sh' in new_list[0]:
                            shell = 'sh'
                        else:
                            '''If it isn't bash or shell we probably don't know what it is.'''
                            continue
                        self.to_test.append({
                            'shell': shell,
                            'path': file
                        })

    def shell_check_files(self):
        for i in self.to_test:
            shell = i['shell']
            file = i['path']
            command = 'shellcheck ' \
                      '--shell={} ' \
                      '--exclude={} ' \
                      '{}'.format(shell, 'SC2086,SC1090', file)
            result, stderr = subprocess.Popen(command,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              shell=True).communicate()
            result = result.decode('utf-8')
            if stderr is None and result is not None and result is not '':
                self.data.shell_check.append([file.replace('/workspace/', ''), result])
        self.data.log_result(
            name='Run shell check for: {}'.format(self.data.docker_name),
            value='PASSED')
