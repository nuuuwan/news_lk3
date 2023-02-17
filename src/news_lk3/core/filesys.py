import os

from utils import Git, get_date_id, hashx, Directory

from news_lk3._utils import log

REPO_DATA_NAME = 'news_lk3_data'
GIT_REPO_URL = f'https://github.com/nuuuwan/{REPO_DATA_NAME}.git'
DIR_ROOT = '/tmp'
DIR_REPO = os.path.join(DIR_ROOT, REPO_DATA_NAME)

SALT = '5568445278803347'
HASH_LENGTH = 8
IGNORE_LIST = ['.git', '.gitignore', '.DS_Store']
SHARD_NAME_LENGTH = 2
ARTICLE_FILE_ONLY_LEN = HASH_LENGTH + 5

def get_hash(url):
    return hashx.md5(url + SALT)[:HASH_LENGTH]


def get_article_file_only(url):
    h = get_hash(url)
    return f'{h}.json'


def get_article_file(url, dir_prefix=''):
    file_name_only = get_article_file_only(url)
    return os.path.join(DIR_REPO, file_name_only)


def git_checkout(force=True):
    log.debug(f'[git_checkout] {force=}')
    git = Git(GIT_REPO_URL)
    git.clone(DIR_REPO, force=force)
    date_id = get_date_id()
    git_branch = f'data-{date_id}'
    git.checkout(git_branch)
    log.debug(f'Cloned {GIT_REPO_URL} [{git_branch}] to {DIR_REPO}')


def get_article_file_paths():
    article_paths = []
    for article_file in Directory(DIR_REPO).children:
        if not article_file.path.endswith('.json'):
            continue
        article_paths.append(article_file.path)
    return article_paths
