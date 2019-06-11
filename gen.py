
import os
import sys
import requests
import getpass


def get_repos():
    url = "https://api.github.com/orgs/wazo-pbx/repos"
    session = requests.Session()
    user = getpass.getpass('GitHub user: ')
    token = getpass.getpass('GitHub password/token: ')
    while True:
        response = session.get(url, headers={
            "Accept": "application/vnd.github.machine-man-preview+json",
            "User-Agent": "PyGithub/Python",
        }, auth=(user, token))
        if response.ok:
            for r in response.json():
                yield r
            if "next" in response.links:
                url = response.links["next"]["url"]
                continue
            else:
                return
        else:
            raise Exception(response.text)

with open("default.xml", 'w') as f:
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<manifest>

    <remote name="origin" fetch="https://github.com" />
    <default revision="refs/heads/master" remote="origin" sync-j="4" />

''')
    for r in get_repos():
        if not r["archived"] and not r['disabled']:
            f.write('    <project name="%(full_name)s" path="%(name)s"/>\n' % r)

    f.write('</manifest>\n')
