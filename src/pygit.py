#!/home/user/location/pygit/venv/bin/python

# Authors:
# MerrinX <knutago1@outlook.com>

import os
import time
import config
import configparser
import multiprocessing
from stringcolor import *
from git import Repo

class Pygit(object):

    def __init__(self, repo: str, user: dict, path: str = ''):
        """
        Pygit initial method
        """
        repo = repo.strip()
        self.path = os.path.join(os.getcwd(), path.strip())
        _ = {'ssh': '', 'name': 'nobody', 'email': 'nobody@mail.com'}
        _.update(user)
        user = _

        if not os.path.isfile(user['ssh']):
            raise Exception(
                f'Missing custom SSH script {user["ssh"]}!\n\n'
                'You must provide a custom SSH script which can be able to execute git commands with the correct SSH key.\n'
                'The bash script should contain this line:\n\n'
                'ssh -i <SSH_private_key> -oIdentitiesOnly=yes -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null "$@"\n\n'
            )

        os.environ['GIT_SSH'] = user['ssh']

        if os.path.isdir(path):
            self.repo = Repo(path)
            print(f'{cs("Fetching update for :", config.YELLOW)} {os.path.basename(path[:-1]):19} Diff :{self.repo.git.pull("origin", "main")}\n')
        else:
            os.makedirs(path)
            self.repo = Repo.clone_from(repo, path, env={'GIT_SSH': user['ssh']})
            self.repo.config_writer().set_value('user', 'name', user['name']).release()
            self.repo.config_writer().set_value('user', 'email', user['email']).release()

    def commit(self, branch: str = 'main', message: str = 'Auto commit'):
        """
        Basic commit method.
        """
        has_changed = False

        for file in self.repo.untracked_files:
            print(f'{cs("Added untracked file:", config.BLUE)} {file} {os.path.basename(self.path[:-1])}\n')
            self.repo.git.add(file)
            has_changed = True

        if self.repo.is_dirty():
            for file in self.repo.git.diff(None, name_only=True).split('\n'):
                if file == '':
                    continue

                print(f'{cs("Added file:", config.BLUE)} {file} {os.path.basename(self.path[:-1])}\n')
                self.repo.git.add(file)
                has_changed = True

        return has_changed

    def remote_repos(output_queue, input_queue, remote_repo, path_repo):
        """
        Common repos method
        """
        user = configparser.ConfigParser()
        user.read('/home/user/path/to/user_cfg')
        repository = Pygit(
                repo = remote_repo,
                user = dict(user.items('user_id')),
                path = path_repo
                )
        if repository.commit() is True:
            output_queue.put(f"\nINPUT: {cs('Write commit msg for ', config.RED)} {os.path.basename(path_repo[:-1])} = ")
            result = input_queue.get()
            repository.repo.git.commit('-m', result)
            repository.repo.git.push('origin', 'main')
        output_queue.put("DONE")

    def run(args):
        process = configparser.ConfigParser()
        process.read('/home/user/path/to/repos.cfg')
        queues = []
        num_processes = 0

        for i, name in enumerate(process):
            if name == "DEFAULT":
                continue
            iq = multiprocessing.Queue()
            oq = multiprocessing.Queue()
            queues.append((iq, oq))
            multiprocessing.Process(target=Pygit.remote_repos, args=(oq, iq, process.get(name, "repo"), process.get(name, "path"))).start()
            num_processes += 1

        done = 0
        waiting_input = 0
        keep = []
        while done + waiting_input < num_processes:
            for iq, oq in queues:
                if not oq.empty():
                    req = oq.get()
                    if "INPUT" in req: 
                        waiting_input += 1
                        keep.append((req, iq))
                    elif "DONE" in req:
                        done += 1
                    else:
                        print(req)
        # Reseting
        done = 0 

        # Keeping inputs until all other processes are done
        for req, iq in keep:
            res = input(req.split(":")[1])
            iq.put(res)

        while done < waiting_input:
            for iq, oq in queues:
                if not oq.empty():
                    req = oq.get()
                    if "DONE" in req:
                        done += 1
                    else:
                        print(req)

        print(cs("\nCompleted Remote Updates", config.GREEN))
