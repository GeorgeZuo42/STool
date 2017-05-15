#!/usr/bin/env python3
# run in python 3.5 and after
import fire
import subprocess
import os
import re
import json
import zipfile
import shutil


class esed(object):
    """An enhanced seed cli."""
    # '$'\n''(input) ->  \\n(code)

    def run(self, command, text, fileName):
        cmd = command + '\\\n' + str(text)
        subprocess.run(
            ["sed", "-i", "*.bak", cmd, fileName], stdout=subprocess.PIPE)

    def append(self, pattern, content, fileName):
        fp = open(fileName)
        isFind = False
        lines = []
        for line in fp:
            lines.append(line)
            if(pattern in line) and not isFind:
                lines.append(content)
                isFind = True
        fp.close()

        fp = open(fileName, 'w')
        fp.write(''.join(lines))
        fp.close()

    def unzip(self, filePath):
        zFile = zipfile.ZipFile(filePath, 'r')
        zFileDir = os.path.dirname(filePath)
        for file in zFile.namelist():
            zFile.extract(file, zFileDir)
        zFile.close()
        os.remove(filePath)
        
    # https://github.com/OmniSharp/omnisharp-vscode/issues/1028 
    def update(self, version="1.8.1", directory=os.getcwd()):
        targetdir = '/Users/HSH/.vscode/extensions/ms-vscode.csharp-%s' % version
        update_list = os.listdir(directory)
        with open(os.path.join(targetdir, "package.json")) as json_file:
            data = json.load(json_file)
            runtimeDependencies = data['runtimeDependencies']
            for unit in runtimeDependencies:
                if 'url' not in unit.keys():
                    continue
                fileName = unit['url'].split('/')[-1]
                if fileName in update_list:
                    fullName = os.path.join(directory, fileName)

                    targetName = os.path.join(
                        targetdir, unit['installPath'].replace("./", ""), fileName)
                    if not os.path.exists(os.path.dirname(targetName)):
                        os.mkdir(os.path.dirname(targetName))
                    shutil.copy(fullName, targetName)
                    self.unzip(targetName)
                    #加上执行权限
                    if 'binaries' in unit.keys():
                        unzipDir = os.path.dirname(targetName)
                        for file in unit['binaries']:
                            file = os.path.join(unzipDir,file.replace("./", ""))
                            subprocess.run(["chmod", "755", file])
        subprocess.run(["touch",os.path.join(targetdir,"install.Lock")])            
        print("success")
        #defaults read ~/Library/Preferences/com.unity3d.UnityEditor5.x.plist | grep RecentlyUsedProjectPaths
if __name__ == '__main__':
    fire.Fire(esed)
