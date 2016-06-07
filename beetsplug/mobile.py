# -*- coding: utf-8 -*-
# This file is part of beets.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Synchronizes songs/albums, with a specific tag, to an external location
"""

from beets import config
from beets.plugins import BeetsPlugin
from beets import ui
from beets.dbcore import types

import os
from os.path import join, getsize
from shutil import copyfile
#from beets.importer import SingletonImportTask

class MobilePlugin(BeetsPlugin):
    def __init__(self):
        super(MobilePlugin, self).__init__()
        self.config.add({
            'query': u'mobile:1',
        })

        #item_types = {'tag': types.STRING}

        if 'directory' in self.config:
            print 'Directory: %s' % self.config['directory'].get()
            self.directory = self.config['directory'].get()
        else:
            print "Please specify a director in the config"
            exit(-1)

        self.query = self.config['query'].get()
        print 'query: %s' % self.query


    def commands(self):

        cmd = ui.Subcommand('mobile', help=u'Sync music to the mobile folder')
        cmd.func = self.run
#        cmd.parser.add_option(
#            u'-l', u'--library', action='store_true',
#            help=u'show library fields instead of tags',
#        )
#        cmd.parser.add_option(
#            u'--append', action='store_true', default=False,
#            help=u'if should append data to the file',
#        )
#        cmd.parser.add_option(
#            u'-i', u'--include-keys', default=[],
#            action='append', dest='included_keys',
#            help=u'comma separated list of keys to show',
#        )
#        cmd.parser.add_option(
#            u'-o', u'--output',
#            help=u'path for the output file. If not given, will print the data'
#        )
        return [cmd]


    def run(self, lib, suboptions, subargs):
        query_result = lib.items(self.query)
        # Walk our directory
        # Build an array of all files
        existing_files = []
        existing_dirs = []
        for root, dirs, files in os.walk(self.directory):
            for d in dirs:
                existing_dirs.append(join(root, d))


        for root, dirs, files in os.walk(self.directory):
            for f in files:
                existing_files.append(join(root, f))

        print "existing files: %s" % existing_files
        print ""
        print "Existing dirs: %s" % existing_dirs

        # Build a list of files to remove
        mobile_songs = []
        for item in query_result:
            relative_path = item.destination(fragment=True)
            dest_file = join(self.directory, relative_path)
            mobile_songs.append(dest_file)


#        print "Mobile_songs: %s" % mobile_songs
        songs_to_delete = []

        for f in existing_files:
            if f not in mobile_songs:
                songs_to_delete.append(f)

        print "Songs to delete: %s" % songs_to_delete

        # Delete the songs
        for f in songs_to_delete:
            print "Delete file: %s" % f.encode('utf-8')
            os.remove(f)

        # Delete any empty directories
        existing_dirs.reverse()
        for d in existing_dirs:
            try:
                print "Trying to remove directory: %s" % d
                os.rmdir(d)
            except OSError as exc:
                pass


        # Copy files to the mobile directory
        for item in query_result:
            # Getting unicode errors so I need to do this:
            # Get the base dir of the main library
            base_dir = config['directory'].get()
            source_file = join(base_dir, item.destination(fragment=True))
            relative_path = item.destination(fragment=True)
            dest_file = join(self.directory, relative_path)

            # Make the directory
            #import pdb;pdb.set_trace()
            print "Making directory: %s" % os.path.dirname(dest_file)
            try:
                os.makedirs(os.path.dirname(dest_file))
            except OSError as exc:
                if exc.errno == os.errno.EEXIST and os.path.isdir(os.path.dirname(dest_file)):
                    pass
                else:
                    raise


            #print "Copying file %s to %s" % (source_file, dest_file)
            #import pdb;pdb.set_trace()
            copyfile(source_file, dest_file)




