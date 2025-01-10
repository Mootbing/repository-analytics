import os
import shutil
from git import Repo # pip install gitpython
import time
from git import RemoteProgress

import urllib.parse

repo_name = ""

# get directory to this file
dir = os.path.dirname(os.path.realpath(__file__))   
repo_path = os.path.join(dir, 'Repo')
clone_repo_y_n = input('Clone a Git repository? (y/n) (if not then runs analysis on current contents of /Repo/ dir): ')

if clone_repo_y_n == 'y':

    repo_url = input('Enter the URL of the repository: ')

    # clear dir /Repo
    def clear_dir():
        print('[Log] Clearing previous directory...')
        # os.chmod(repo_path, 0o777)
        shutil.rmtree(repo_path)

    # clone repo
    class CloneProgress(RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
            if message:
                print(message)

    def clone_repo(repo_url):
        global repo_name
        print('[Log] Cloning repository...')
        Repo.clone_from(repo_url, repo_path, progress=CloneProgress())

        repo_name = repo_url.split('/')[-1].split('.')[0]
        print('[Log] Repository cloned successfully')

    if os.path.exists(repo_path):
        clear_dir()

    os.mkdir(repo_path)

    clone_repo(repo_url)

# .ext : {linecount, filecount}
fileExtensionsCounter = {}
errors_count = 0

default = {
    "line count": 0,
    "file count": 0
}

# analysis
def recursiveAnalytics(repo_path):
    global errors_count

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
                    errors_count += 1
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
    global repo_name

    if repo_name == "":
        repo_name = input('Enter the name of the repository: ')

    with open(os.path.join(dir, 'Analytics.md'), 'w+') as f:

        # f.write("## # of Files Per Extension:\n")
        file_counter = []
        line_counter_per_file = []
        ext_array = []
        
        total_lines = 0
        for ext in fileExtensionsSortedByFileCount():
            # f.write(f".{ext[0]} : {ext[1]['file count']}\n\n")

            ext_array.append(ext[0])
            file_counter.append(ext[1]['file count'])
            line_counter_per_file.append(ext[1]['line count'])

            total_lines += ext[1]['line count']

        print(file_counter)
        print(line_counter_per_file)
        print(ext_array)
        
        ext_array = ','.join(map(str, ext_array))
        file_counter_str = ','.join(map(str, file_counter))
        line_counter_per_file_str = ','.join(map(str, line_counter_per_file))

        # print(file_counter_str)
        # print(line_counter_per_file_str)

        f.write(f"""\n\n# Code Analysis of {repo_name} \n\n""")
        svg_src = (f"""<img src="https://repo-analytics-backend.vercel.app/api?backgroundColor=black
&titleColor=white
&textColor=white
&subHeader={urllib.parse.quote(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))}
&title={
    urllib.parse.quote("Analysis of '" + repo_name + "'")
}
&numFiles={len(fileExtensionsCounter)}
&totalLines={total_lines}
&errors={errors_count}
&extensions={urllib.parse.quote(ext_array)}
&fileCounter={urllib.parse.quote(file_counter_str)}
&lineCounterPerFile={urllib.parse.quote(line_counter_per_file_str)}"
 alt="Code Analysis" />
""".replace('\n', ''))
        
        f.write(svg_src)

writeResults()
print("[Log] Results written to Analytics.md")