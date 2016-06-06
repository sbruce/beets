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
#from beets.importer import SingletonImportTask

class MobilePlugin(BeetsPlugin):
    def __init__(self):
        super(MobilePlugin, self).__init__()
        self.config.add({
            'query': 'tag:mobile',
        })
        
        item_types = {'tag': types.STRING}        
        
        if 'directory' in self.config:
            print 'Directory: %s' % self.config['directory'].get()
            
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
        for i in lib.items(self.query):
            print i

            
