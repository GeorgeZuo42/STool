#!/usr/bin/env python3
# run in python 3.5 and after
import fire
import subprocess
import os
import re


class esvn(object):
    """An enhanced svn cli."""

    def _getStatus(self, directory):
        result = subprocess.run(
            ["svn", "st", directory], stdout=subprocess.PIPE)
        fileList = {}
        pattern = re.compile(r' +')
        for r in result.stdout.decode().split('\n'):
            if r == '':
                continue
            words = pattern.split(r)
            if len(words[0]) > 1:
                continue
            if words[0] not in fileList:
                fileList[words[0]] = list()
            fileList[words[0]].append(words[1])
        return fileList

    def up(self, directory=os.getcwd()):
        result = subprocess.run(
            ["svn", "up", directory], stdout=subprocess.PIPE)
        print(result.stdout.decode())

    def st(self, tag="",directory=os.getcwd()):
        for k,v in self._getStatus(directory).items():
            if(k == tag or tag==""):
                print('\n'.join(v))

    def ci(self, comment, directory=os.getcwd()):
        fileList = self._getStatus(directory)
        if '?' in fileList:
            subprocess.run(["svn", "add", ' '.join(fileList['?'])])
        if '!' in fileList:
            subprocess.run(["svn", "del", ' '.join(fileList['!'])])
        comment = 'Author: ZuoQi\nContent: ' + comment
        subprocess.run(["svn", "ci", directory, "-m", comment])

    def cleanup(self,directory=os.getcwd()):
        subprocess.run(["svn", "cleanup", "--include-externals","--remove-unversioned",directory])
        subprocess.run(["svn", "revert", "-R",directory])
if __name__ == '__main__':
    fire.Fire(esvn)
