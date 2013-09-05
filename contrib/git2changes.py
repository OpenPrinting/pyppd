#!/usr/bin/python
# Copyright 2010 Vitor Baptista <vitor@vitorbaptista.com>
# Distributed under the terms of the GNU Lesser General Public License v3 or later

from subprocess import Popen, PIPE
import re

class Commit:
    def __init__(self, log):
        log.strip()
        log_array = log.split('\n')
        self.commit = log_array.pop(0).split('commit ')[0]
        self.author = log_array.pop(0).split('Author: ')[1]
        self.date = log_array.pop(0).split('Date:   ')[1]

        # Remove garbage from array
        while True:
            garbage = log_array.pop()
            if re.search(r'files? changed', garbage): break

        self.changed_files = []
        changed_file = log_array.pop()
        while changed_file != "":
            self.changed_files += [changed_file.split('|')[0].strip()]
            changed_file = log_array.pop()

        self.message = ""
        try:
            while True:
                commit_line = log_array.pop().strip()
                if (commit_line == "" or
                    commit_line.find('Signed-off-by') != -1 or
                    commit_line.find('git-svn-id') != -1):
                    commit_line = log_array.pop()
                    continue
                self.message = commit_line.strip() + " " + self.message
        except IndexError:
            pass

        self.message = self.__break_string(self.message, 80)

        self.version = None

    def __break_string(self, string, column):
        finished_string = ""
        string = string.replace('\n', ' ')
        while column < len(string):
            break_point = string[0:column].rfind(' ')
            if break_point == -1:
                break_point = string[column + 1:].find(' ')
                if break_point != -1:
                    break_point += column

            finished_string += string[0:break_point] + "\n"
            string = string[break_point + 1:]

        if string != "": finished_string += string

        return finished_string


    def __str__(self):
        message_with_files = '* ' + ', '.join(self.changed_files) + ': ' + self.message
        message_with_files = self.__break_string(message_with_files, 78)
        message_with_files = '  ' + message_with_files.replace('\n', '\n  ')
        if message_with_files[-1] == ' ': message_with_files = message_with_files[0:-1]
        return message_with_files


def get_version(commit):
    setup_py = Popen(["git", "show", "%s:setup.py" % commit], stdout=PIPE).communicate()[0]
    version = setup_py.split("version='")[1].split("'")[0]
    return version

def run(output):
    log = Popen(["git", "log", "--summary", "--stat", "--no-merges", "--date=short"], stdout=PIPE).communicate()[0]
    log = "\n%s" % log
    log_array = re.split('\ncommit ', log)
    log_array.pop(0)
    commits = []
    for commit in log_array:
        commits.insert(0, Commit(commit))

    prevVersion = ""
    for commit in commits:
        version = get_version(commit.commit)
        if prevVersion == "" or version != prevVersion:
            commit.version = version
        prevVersion = version

    commits.reverse()
    if not commits[0].version: commits[0].version = "HEAD"
    for commit in commits:
        if commit.version:
            output_format = "v%s (%s)\n\n"
            if commit.version == "HEAD": output_format = "%s (%s)\n\n"
            output.write(output_format % (commit.version, commit.date))
        output.write("%s\n\n" % commit)


if __name__ == "__main__":
    from sys import stdout
    run(stdout)
    stdout.close()
