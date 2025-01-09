import os
import shutil
from git import Repo # pip install gitpython
import time
from git import RemoteProgress

import urllib.parse

# get directory to this file
dir = os.path.dirname(os.path.realpath(__file__))   
repo_path = os.path.join(dir, 'Repo')
clone_repo_y_n = input('Clone a repository? (y/n) (if not then runs analysis on current contents of /Repo/ dir): ')

if clone_repo_y_n == 'y':

    repo_url = input('Enter the URL of the repository: ')

    # clear dir /Repo
    def clear_dir():
        print('[Log] Clearing previous directory...')
        shutil.rmtree(repo_path)

    # clone repo
    class CloneProgress(RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
            if message:
                print(message)

    def clone_repo(repo_url):
        print('[Log] Cloning repository...')
        Repo.clone_from(repo_url, repo_path, progress=CloneProgress())
        print('[Log] Repository cloned successfully')

    clear_dir()
    os.mkdir(repo_path)

    clone_repo(repo_url)

# .ext : {linecount, filecount}
fileExtensionsCounter = {}

default = {
    "line count": 0,
    "file count": 0
}

# analysis
def recursiveAnalytics(repo_path):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            # exclude files and directories beginning with a .
            if file.startswith('.') or root.startswith('.'):
                continue

            # get file extension
            ext = file.split('.')[-1]

            # count file extensions
            if ext in fileExtensionsCounter:
                fileExtensionsCounter[ext]["file count"] += 1
            else:
                fileExtensionsCounter[ext] = default.copy()
                fileExtensionsCounter[ext]["file count"] += 1

            # count lines of code
            with open(os.path.join(root, file), 'r') as f:

                try: 
                    file_contents = f.readlines()
                    fileExtensionsCounter[ext]["line count"] += len(file_contents)
                except:
                    print("[Error] Could not analyze file: " + os.path.join(root, file))
                    continue

            print("[Analyzing] " + os.path.join(root, file))

def prune_last_results_md():
    if os.path.exists(os.path.join(dir, 'results.md')):
        os.remove(os.path.join(dir, 'results.md'))

prune_last_results_md()

recursiveAnalytics(repo_path)

def fileExtensionsSortedByFileCount():
    return list(sorted(fileExtensionsCounter.items(), key=lambda x: x[1]["file count"], reverse=True))

def fileExtensionsSortedByLineCount():
    return list(sorted(fileExtensionsCounter.items(), key=lambda x: x[1]["line count"], reverse=True))

# write results to file
def writeResults():
    with open(os.path.join(dir, 'README.md'), 'w+') as f:
        f.write("# File Type Analytics\n")
        f.write("## # of Files:\n" + str(len(fileExtensionsCounter)) + "\n\n")

        f.write("## # of Files Per Extension:\n")
        for ext in fileExtensionsSortedByFileCount():
            f.write(f".{ext[0]} : {ext[1]['file count']}\n\n")

        total_lines = 0
        for ext in fileExtensionsCounter:
            total_lines += fileExtensionsCounter[ext]["line count"]

        f.write("\n## # of Lines Per Extension: \n")
        for ext in fileExtensionsSortedByLineCount():
            f.write(f".{ext[0]} : {ext[1]['line count']}\n\n")

        f.write("\n## Total File Lines: \n")
        f.write(str(total_lines))

        f.write("\n\n# Code Analysis SVG\n")
        f.write(f"""
<img src="https://repo-analytics-backend.vercel.app/api?backgroundColor=black&titleColor=white&textColor=white&title={
    urllib.parse.quote("Code Analysis On " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
}&numFiles={len(fileExtensionsCounter)}&totalLines={total_lines}" alt="Code Analysis" />
""")

writeResults()
print("[Log] Results written to README.md")