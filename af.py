#!/usr/local/bin/python3

import os
import sys
import gitlab
import json
import subprocess
from pathlib import Path
from slugify import slugify

os.system("clear")

# Args
args = sys.argv[1:]

# Config
CONFIG_FILE = "{}/.airfleet-cli".format(str(Path.home()))
CONFIG      = {}

# Line
LINE = "------------------------------"

# Terminal Colors
def color(color, text):
    colors = {
        "end"       : '\033[0m',
        "red"       : '\033[0;31m',
        "green"     : '\033[0;32m',
        "orange"    : '\033[0;33m',
        "blue"      : '\033[0;34m',
        "lightblue" : '\033[1;34m',
        "lightgray" : '\033[0;37m',
        "darkgray"  : '\033[1;30m',
        "yellow"    : '\033[1;33m',
        "white"     : '\033[1;37m',
        "cyan"      : '\033[0;36m',
        "purple"    : '\033[0;35m',
    }
    return "{}{}{}".format(colors[color], text, colors["end"])


# Exec Command
def exec(cmd):
    try:
        out = str( subprocess.check_output(" ".join(cmd), shell=True).decode() ).strip()
        return out
    except Exception as e:
        print(color("red", str(e)))
        return None


# Check Config
if not os.path.isfile(CONFIG_FILE):
    print()
    print(color("cyan", "INITIAL SETUP"))
    print(color("darkgray", LINE))
    print("{} {}".format(color("darkgray", "1."), "Go to {}".format(color("white", "https://gitlab.com/profile/personal_access_tokens"))))
    print("{} {}".format(color("darkgray", "2."), "Enter a name for your token."))
    print("{} {}".format(color("darkgray", "3."), "Check `{}` from scopes.".format(color("white", 'api'))))
    print("{} {}".format(color("darkgray", "4."), "Click `{}` button.".format(color("white", 'Create personal access token'))))
    print("{} {}".format(color("darkgray", "4."), "Copy your access token."))
    print(color("darkgray", LINE))
    print()
    config_token = input( "{}{}".format( color("green", "Gitlab Access Token"), color("darkgray", " : ") ) )

    os.system("clear")
    print()
    print(color("cyan", "INITIAL SETUP"))
    print(color("darkgray", LINE))
    print("{} {}".format(color("darkgray", "-"), "Please enter your username/nickname."))
    print("{} {}".format(color("darkgray", "-"), "This is for the branch names for each task."))
    print(color("darkgray", LINE))
    print("{} {}".format(color("darkgray", "-"), "{} mustafa-aydemir".format( color( "cyan", "Example{}".format( color("darkgray", ":") ) ) ) ) )
    print(color("darkgray", LINE))
    print()
    config_username = input( "{}{}".format( color("green", "Username"), color("darkgray", " : ") ) )
    config_username = slugify(config_username)

    CONFIG = {
        "token"    : config_token,
        "username" : config_username,
    }

    json_config = json.dumps(CONFIG)
    with open(CONFIG_FILE, 'w') as out:
        out.write(json_config + "\n")
    os.system("clear")

else:
    json_config = open(CONFIG_FILE, 'r').read().strip()
    CONFIG = json.loads(json_config)


# Gitlab
gl = gitlab.Gitlab('https://gitlab.com', private_token = CONFIG['token'])
gl.auth()

# Gitlab Info
user     = gl.user
project  = False
projects = gl.projects.list(visibility='private')

# Repo User
repo_user = {
    "name"  : exec(["git", "config", "--global", "user.name"]),
    "email" : exec(["git", "config", "--global", "user.email"]),
}

# Repo
repo_remote = exec(["git", "config", "--get", "remote.origin.url"])

# Project
for p in projects:
    if p.ssh_url_to_repo == repo_remote:
        project = p
        break

# Branches
branches = exec(["git", "branch"])

# Current Branch
curr_branch = None
if branches:
    for i in branches.splitlines():
        if i.startswith("*"):
            curr_branch = i.replace("*", "").strip()
            break

# MRs
mrs     = project.mergerequests.list(state = 'opened')
mr_list = {}

if mrs:
    for i in mrs:
        if i.source_branch == curr_branch:
            mr_list[i.target_branch] = i.web_url

def update_mrs():

    global mrs
    global mr_list

    # MRs
    mrs = project.mergerequests.list(state = 'opened')

    if mrs:
        for i in mrs:
            if i.source_branch == curr_branch:
                mr_list[i.target_branch] = i.web_url


def print_user():
    print()
    print(color("cyan", "CURRENT USER"))
    print(color("darkgray", LINE))
    print("{} {} {}".format( color("orange", "User"), color("darkgray", " :"), repo_user['name'] ))
    print("{} {} {}".format( color("orange", "Email"), color("darkgray", ":"), repo_user['email'] ))

def print_repo():
    print()
    print(color("cyan", "CURRENT REPOSITORY"))
    print(color("darkgray", LINE))
    print("{} {} {}".format( color("orange", "ID"), color("darkgray", "            :"), color("cyan", project.id) ))
    print("{} {} {}".format( color("orange", "URL"), color("darkgray", "           :"), color("cyan", project.web_url) ))
    print("{} {} {}".format( color("orange", "Name"), color("darkgray", "          :"), color("green", project.name_with_namespace) ))
    print("{} {} {}".format( color("orange", "Current Branch"), color("darkgray", ":"), color("lightblue", curr_branch) ))
    print("{} {} {}".format( color("orange", "Created At"), color("darkgray", "    :"), color("darkgray", project.created_at) ))
    print("{} {} {}".format( color("orange", "Last Activity"), color("darkgray", " :"), color("darkgray", project.last_activity_at) ))

def print_mrs(label = "Open MRs"):
    print()
    print(color("cyan", label))
    print(color("darkgray", LINE))

    if len(mr_list) == 0:
        print(color("purple", "No MR created for this branch."))

    else:
        # Max Space
        max_space = 0
        for k, v in mr_list.items():
            if len(k) > max_space:
                max_space = len(k)

        # MRs
        for k, v in mr_list.items():
            space = " ".join([ "" for i in range(0, max_space + 1 - len(k)) ])
            print("{} {} {}".format( color("orange", k.title()), color("darkgray", space + ":"), color("cyan", v) ))


def create_task():
    print()
    print(color("cyan", "CREATE BRANCH FOR NEW TASK"))
    print(color("darkgray", "---------------------------------------------------"))
    print("{} {} {task}/{id}/{title}/{user}/{source}".format(
        color("orange", "Branch Template"),
        color("darkgray", ":"),
        task   = color('darkgray', "{}".format( color("lightgray", "task") )),
        id     = color('darkgray', "{}{}{}".format( color("darkgray", "{"), color("orange", "id"), color("darkgray", "}") )),
        title  = color('darkgray', "{}{}{}".format( color("darkgray", "{"), color("blue", "title"), color("darkgray", "}") )),
        user   = color('darkgray', "{}{}{}".format( color("darkgray", "{"), color("green", "user"), color("darkgray", "}") )),
        source = color('darkgray', "{}{}{}".format( color("darkgray", "{"), color("cyan", "source"), color("darkgray", "}") )),
        ))

    print(color("darkgray", "---------------------------------------------------"))
    print()

    id    = False
    title = False

    while not id:
        id = input( "{}{}".format( color("orange", "ID"), color("darkgray", "     : ") ) )
    
    while not title:
        title = input( "{}{}".format( color("blue", "Title"), color("darkgray", "  : ") ) )

    user   = input( "{}{}".format( color("green", "User"), color("darkgray", "   : ({}) ".format(CONFIG['username'])) ) )
    source = input( "{}{}".format( color("cyan", "Source"), color("darkgray", " : (origin/master) ") ) )
    print()

    if not user:
        user = CONFIG['username']

    if not source:
        source = "origin/master"

    _source = source
    if source.startswith("origin/"):
        _source = source[7:]

    title = slugify(title)
    source_slug = slugify(_source)

    new_branch = "{task}/{id}/{title}/{user}/{source}".format(
        task   = "task",
        id     = id,
        title  = slugify(title),
        user   = user,
        source = slugify(source_slug),
        )

    # Check Status
    git_status = int(str(exec(["git status | grep modified: | wc -l"])))

    if git_status > 0:
        print()
        print(color("red", "== ERROR ========================="))
        print(color("red", "Please commit your changes or stash them before you switch branches."))

    else:
        # Create Branch
        create_branch = exec(["git checkout -b '{}' '{}'".format(new_branch, source)])

        dyline = "-".join( [ "" for i in range(0, len(new_branch) + 20) ] )
        print()
        print( color("green", dyline) )
        print( color("green", "--- CREATED -- ") + new_branch + color("green", " ---") )
        print( color("green", dyline) )


if __name__ == "__main__":

    # Overview
    if len(args) == 0:
        print_user()
        print_repo()
        print_mrs()

    # MRs
    elif len(args) >= 1 and args[0] == "mr":
        title = curr_branch

        if len(args) == 1:
            print_mrs()

        elif len(args) >= 2 and args[0] == "mr":

            if len(args) == 3:
                title = args[2]

            if args[1] in mr_list:
                print("")
                print(color("red", "! ============================= !"))
                print(color("red", "! == THIS MR ALREADY EXISTS! == !"))
                print(color("red", "! ============================= !"))
                print_mrs()
            
            else:
                create_mr = project.mergerequests.create({
                    'source_branch' : curr_branch,
                    'target_branch' : args[1],
                    'title'         : title,
                })

                print("")
                print(color("green", "! ============================= !"))
                print(color("green", "! ======== MR CREATED! ======== !"))
                print(color("green", "! ============================= !"))

                update_mrs()
                print_mrs("MRs")

    elif len(args) >= 1 and args[0] == "branch":
        create_task()


print("")