#!/usr/bin/env python

# Get all pull requests comments from a user on a github repo
from csv import DictWriter

from github import GitHub  # pip install githubpy==1.1.0

CSV_FIELD_NAMES = ['message', 'url', 'username']
# TODO make these command line args with defaults
GITHUB_ACCESS_TOKEN = '<your token>'
OWNER = 'pbs'
REPO = ''
USER = ''


def get_comments(owner, repo, user, csvfile):
    gh = GitHub(access_token=GITHUB_ACCESS_TOKEN)
    page = 1
    writer = DictWriter(csvfile, fieldnames=CSV_FIELD_NAMES)
    writer.writeheader()

    while True:
        print "Getting page {}".format(page)
        new_comments = gh.repos(owner)(repo).pulls.comments.get(page=page)
        if len(new_comments) == 0:
            break
        else:
            page = page + 1
        for comment in new_comments:
            if comment['user']['login'] == user:
                row = {
                    'message': comment['body'].encode('utf8'),
                    'url': comment['html_url'],
                    'username': comment['user']['login']
                }
                writer.writerow(row)


if __name__ == "__main__":
    filename = "pull-request-comments-{}-{}-{}.csv".format(OWNER, REPO, USER)
    with open(filename, 'w') as f:
        get_comments(OWNER, REPO, USER, f)
