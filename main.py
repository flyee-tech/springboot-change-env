import os
import operator
import re
import sys
from configparser import ConfigParser
import yaml

import pandas as pd
import pymysql
from rich.console import Console
from rich.table import Table

console = Console()
workspace_path = '/Users/peiel/IdeaProjects/youlu/myspringcloud/'

def get_config(env):
    with open("./conf_%s.yml" % env) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def get_config_by_path(path):
        with open(path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

def search_source_file():
    find_list = list()
    find_name = 'bootstrap-dev.yml'
    for root, dirs, files in os.walk(workspace_path):
        if 'resources' in root and find_name in files:
            find_list.append(root + '/' + find_name)
    return find_list

def replace_rabbit(dict_conf, dict_source):
    if 'rabbitmq' in dict_source['spring'] and 'rabbitmq' in dict_conf['spring']:
        dict_source['spring']['rabbitmq'] = dict_conf['spring']['rabbitmq']
    return dict_source

def replace_redis(dict_conf, dict_source):
    if 'redis' in dict_source['spring'] and 'redis' in dict_conf['spring']:
        dict_source['spring']['redis'] = dict_conf['spring']['redis']
    return dict_source

def replace_db(dict_conf, dict_source):
    if 'datasource' in dict_source['spring'] and 'datasource' in dict_conf['spring']:
        dict_source['spring']['datasource'] = dict_conf['spring']['datasource']
    return dict_source

def write(path, data):
    with open(path, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    if len(sys.argv) != 2 or (sys.argv[1] != 'dev' and sys.argv[1] != 'uat'):
        console.print("[red]参数校验失败，输入格式：python main.py [环境]]")
        console.print("[cyan]例如：python main.py dev")
        exit()

    find_list = search_source_file()
    conf = get_config(sys.argv[1])
    for source_path in find_list:
        dict_data = replace_rabbit(conf, get_config_by_path(source_path))
        dict_data = replace_redis(conf, dict_data)
        dict_data = replace_db(conf, dict_data)
        data = yaml.dump(dict_data)
        data = data.replace("null", "")
        write(source_path, data)
        print(source_path)
        os.system('cd %s ;git update-index --skip-worktree %s' % (workspace_path, source_path))
