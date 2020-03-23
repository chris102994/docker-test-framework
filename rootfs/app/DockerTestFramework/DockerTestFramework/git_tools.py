'''
GitHub Push tools
'''

import os

from DockerTestFramework.data_classes import ENVars
from github import Github, GithubException


class GitTools:
    commit_message: str
    data: ENVars
    git_session: Github
    file_list: []

    def __init__(self, data: ENVars = None):
        if data is None:
            raise Exception('SeleniumTools Should not be called without ENVars object as the argument.')
        else:
            self.data = data
        self.git_session = Github(self.data.git_username, self.data.git_token)
        self.git_repo = self.git_session.get_user().get_repo('chris102994.github.io')
        self.file_list = os.listdir(self.data.out_dir)
        self.file_list[:] = ['{}/{}'.format(self.data.git_dir, file) for file in self.file_list]
        self.commit_message = 'CI Update of {} tag {}'.format(self.data.docker_name, self.data.git_version)

    def update_ci_repo(self):
        print('Updating CI report on github.')
        for file in self.file_list:
            with open(file, 'rb') as fd:
                contents = fd.read()
            try:
                self.git_repo.create_file(
                    path=file,
                    message='Start tracking {!r}'.format(file),
                    content=contents
                )
            except GithubException:
                print('File {} exists. Updating.'.format(file))
                sha = self.git_repo.get_contents(path=file).sha
                self.git_repo.update_file(
                    path=file,
                    message='Updating existing file {}.'.format(file),
                    content=contents,
                    sha=sha
                )

        print('Finished Updating CI report on github.')
        pass
