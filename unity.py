#!/usr/bin/env python3
# run in python 3.5 and after
import fire
import subprocess
import os
import re
import signal
import time
import sys

class unity(object):
    """An enhanced unity cli."""

    def open(self):
        result = subprocess.run(
            ["defaults", "read", "/Users/HSH/Library/Preferences/com.unity3d.UnityEditor5.x.plist"], stdout=subprocess.PIPE)
        unity = "/Applications/Unity5.3.7/Unity.app/Contents/MacOS/Unity"
        # print(result)
        projects = {}
        for line in result.stdout.decode().split('\n'):
            if "RecentlyUsedProjectPaths" in line:
                number = line.split('=')[0].strip(' "').split('-')[1]
                projects[number] = line.split('=')[1].strip(' ";')
        print("Select the project you want to open :")
        for x, y in projects.items():
            print("    %s : %s" % (x, y))
        r = input('number:')
        if r in projects.keys():
            print(projects[r])
        signal.signal(signal.SIGINT, handler)
        subprocess.Popen([unity, "-projectPath", projects[r]])


def handler(signum, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == '__main__':
    fire.Fire(unity)
