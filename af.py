#!/usr/local/bin/python3

import os
import sys
import gitlab
import subprocess
from slugify import slugify

os.system("clear")

# Args
args = sys.argv[1:]

# Logs
LOGS = []

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


# Gitlab
gl = gitlab.Gitlab('https://gitlab.com', private_token='iYPaj7R2yV61Z8m7ZQBx')
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

    user   = input( "{}{}".format( color("green", "User"), color("darkgray", "   : (mustafa) ") ) )
    source = input( "{}{}".format( color("cyan", "Source"), color("darkgray", " : (origin/master) ") ) )
    print()

    if not user:
        user = "mustafa"

    if not source:
        source = "origin/master"

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