from fabric.api import *


env.backup_db_list = [{'engine': 'mysql',
                       'name': 'timeline',
                       'user': 'root',
                       'password': 'root',
                       'host': '10.135.50.43'},
                       ]

env.backup_remote_store = {'user': 'root',
                           'password': 'root',
                           'host': '10.135.50.43',
                           'port': '22',
                           'path': '/home/user/myproject/djcmsTimelineJS/djcmstimelinejs',
                           'mount_point': 'backup',
                           'sub_path_db': 'db',
                           'sub_path_files': 'static'}

env.backup_files_list = [{'localpath': 'uploads',
                          'excludes': ['_*', '__*']},
                        ]