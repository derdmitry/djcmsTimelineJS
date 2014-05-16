
from fabric.api import *

import os
import time


__all__ = ['backup_db', 'backup_files']


def mysqldump(db):
    date = time.strftime('%Y%m%d')
    dump_file = '/tmp/%(database)s-%(host)s-%(date)s.sql' % {'database': db['name'],
                                                             'host':db['host'],
                                                            'date': date}
    db['dump_file'] = dump_file

    local('mysqldump --no-create-db --opt '
          '--user=%(user)s --password=%(password)s '
          '--host=%(host)s %(name)s > %(dump_file)s' % db)

    return dump_file


def psqldump(db):
    pass


def mongodbdump(db):
    """
    mongoexport -db wimoto_stage --collection entry_categories --out entry_categories.json
mongoexport -db wimoto_stage --collection entries --out entries.json

    run("mongoimport --db {0} --collection {1} {2};".format(
        MONGO_DB_NAME, splited[0], file_path))

    """
    pass


db_engine_dict = {'mysql': mysqldump,
                  'postgresql': psqldump,
                  'mongodb': mongodbdump}


def make_local_dumps():
    dump_file_list = []

    for db in env.backup_db_list:
        dump_function = db_engine_dict[db['engine']]
        dump_file = dump_function(db)
        dump_file_list.append(dump_file)

    return dump_file_list


def mount_remote_store_with_pass():
    mount_point = env.backup_remote_store['mount_point']
    if not os.path.exists(mount_point):
        local('mkdir -p %s' % mount_point)

    local("echo '%(password)s' | "
          "sshfs -o port=%(port)s %(user)s@%(host)s:/%(path)s %(mount_point)s"
          " -o password_stdin" % env.backup_remote_store)

    return mount_point

def mount_remote_store():
    mount_points = []
    for backup_remote_store in env.backup_remote_store:
        mount_point = "%s-%s" % (backup_remote_store['host'],
                                 backup_remote_store['mount_point'])

        if not os.path.exists(mount_point):
            local('mkdir -p %s' % mount_point)
        backup_remote_store['mount_point'] = mount_point
        local("echo '%(password)s' | "
              "sshfs -o port=%(port)s %(user)s@%(host)s:/%(path)s %(mount_point)s" % backup_remote_store)

        mount_points.append(mount_point)

    return mount_points

def umount_remote_store():
    for backup_remote_store in env.backup_remote_store:
        local("fusermount -u %s" % backup_remote_store['mount_point'])


def copy_dumps_to_remote_store(dump_file_list):

    for i, remote_store_path in enumerate(mount_remote_store()):
        date = time.strftime('%Y%m%d')
        remote_dump_path = os.path.join(remote_store_path,
                                        env.backup_remote_store[i]['sub_path_db'],
                                        date)

        if not os.path.exists(remote_dump_path):
            local('mkdir -p %s' % remote_dump_path)

        for dump_file in dump_file_list:
            basename_dump_file = os.path.basename(dump_file)
            remote_dump_file = os.path.join(remote_dump_path, basename_dump_file)
            local("cp %s %s" % (dump_file, remote_dump_file))
            for local_path in env.backup_files_list:
                local_dump_file = os.path.join(local_path['localpath'], basename_dump_file)
                local("cp %s %s" % (remote_dump_file, local_dump_file))

        print "copy dump: cp %s %s" % (dump_file, remote_dump_file)
    umount_remote_store()

@parallel
def backup_db():
    dump_file_list = make_local_dumps()
    print "Files list: \n", dump_file_list
    copy_dumps_to_remote_store(dump_file_list)

@parallel
def backup_files():

    remote_store_path = mount_remote_store()
    date = time.strftime('%Y%W')
    remote_dump_path = os.path.join(remote_store_path,
                                    env.backup_remote_store['sub_path_files'],
                                    date)

    if not os.path.exists(remote_dump_path):
        local('mkdir -p %s' % remote_dump_path)

    for backup_files in env.backup_files_list:
        excludes = ''
        if backup_files.get('excludes'):
            excludes = ' '.join(["--exclude '%s'" % e for e in backup_files['excludes']])
        local('rsync -r -v --delete %s %s %s' %
              (excludes, remote_dump_path, backup_files['localpath']))
    print 'rsync -r -v --delete %s %s %s' % (excludes, remote_dump_path, backup_files['localpath'])
    umount_remote_store()
