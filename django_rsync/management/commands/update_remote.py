# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import subprocess
from django.core.management.base import BaseCommand, CommandError
if sys.version_info < (3, 0):
    from ConfigParser import SafeConfigParser as ConfigParser, NoSectionError
else:
    from configparser import ConfigParser, NoSectionError
    



class Command(BaseCommand):
    args = u'<config_file.ini>'
    help = u'''
Rsync to remote server excluding .svn/, .git/, .hg, and all configured files 
and folders in filters file
'''
    
    def handle(self, *args, **options):
        config = ConfigParser()
        try:
            self.stdout.write(u'Starting sync from '+args[0])
            config.read(args[0])
            remote_user = config.get('remote', 'user')
            remote_host = config.get('remote', 'host')
            remote_port = config.get('remote', 'port')
            remote_dir  = config.get('remote', 'dir')
            
            rsync_cmd = 'rsync -e "/usr/bin/ssh -p  ' + remote_port + '" --cvs-exclude -a --progress --stats --delete -l -z -v -r -p ./ ' + remote_user + '@' + remote_host + ':' + remote_dir
            try:
                exclude_file = config.get('rsync_conf', 'exclude_file')
                rsync_cmd += ' --exclude-from "'+exclude_file+'"'
            except:
                print "Exclude file not loaded"
            try:
                include_file = config.get('rsync_conf', 'include_file')
                rsync_cmd += ' --include-from "'+include_file+'"'
            except:
                print "Include file not loaded"
            try:
                filter_file = config.get('rsync_conf', 'filter_file')
                rsync_cmd += ' --filter "merge '+filter_file+'"'
            except:
                print "Filter file not loaded"
            
            code=subprocess.call(rsync_cmd, shell=True)
            
            if code != 0:
                final_message=u'There were an rsync error, please, check your config'
            else:
                final_message=u'Sync Ok.'
        except IndexError:
            final_message=u'''
You must provide a valid config file for server and sync configuration.
Usage: ./manage.py update_remote file_path.ini
            '''
        except NoSectionError:
            final_message=u'''
You must provide a valid config file for server and sync configuration.
The file must have a valid config format. See doc for more info.
            '''
        finally:
            self.stdout.write(final_message)
            
            
    