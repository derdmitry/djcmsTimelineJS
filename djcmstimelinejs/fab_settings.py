from fabric.api import *


env.backup_db_list = [{'engine': 'mysql',
                       'name': 'timeline',
                       'user': 'root',
                       'password': 'root',
                       'host': '10.135.50.43'},
                      # {'engine': 'postgresql',
                      #  'name': '',
                      #  'user': 'root',
                      #  'password': 'root',
                      #  'host': 'localhost'}
                       ]

env.backup_remote_store = {'user': 'root',
                           'password': 'root',
                           'host': '10.135.50.43',
                           'port': '22',
                           'path': '',
                           'mount_point': 'backup',
                           'sub_path_db': 'db',
                           'sub_path_files': 'files'}

env.backup_files_list = [{'localpath': 'uploads',
                          'excludes': ['_*', '__*']},
                        ]