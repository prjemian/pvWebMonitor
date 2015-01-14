#!/usr/bin/env python

'''
pv2web_ro.main

USAGE::

    jemian@gov:~$ pv2web_ro
    usage: pv2web_ro [-h] [-l LOG_FILE] [-v] xml_config_file
    pv2web_ro: error: too few arguments

HELP::

    jemian@gov:~$ pv2web_ro -h
    usage: pv2web_ro [-h] [-l LOG_FILE] [-v] [--setup SETUP] xml_config_file
    
    pv2web_ro: post EPICS PVs to read-only web page
    
    positional arguments:
      xml_config_file       XML configuration file
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LOG_FILE, --log_file LOG_FILE
                            log file
      -v, --version         show program's version number and exit
    
    getting started (none of the above):
      --setup SETUP         setup a new project directory

VERSION::

    jemian@gov:~$ pv2web_ro -v
    2015.0112.0

'''

# Copyright (c) 2005-2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import logging
import sys

import pv2web_ro
import pvwatch
import utils

DEFAULT_LOG_FILE = 'log_file.txt'


def main():
    '''entry point for the command-line interface'''
    import argparse
    import read_config
    
    doc = pv2web_ro.__package_name__
    doc += ': ' + pv2web_ro.__description__
    
    parser = argparse.ArgumentParser(description=doc)

    if '--setup' not in sys.argv:
        parser.add_argument('xml_config_file', 
                        action='store', 
                        help="XML configuration file",
                        default='configuration.xml')

        parser.add_argument('-l', '--log_file', 
                            action='store', 
                            help="log file",
                            default='log_file.txt')
        
        parser.add_argument('-v', '--version', 
                            action='version', 
                            version=pv2web_ro.__version__)

    group = parser.add_argument_group('getting started (none of the above)')
    group.add_argument('--setup', 
                        help="setup a new project directory",
                        type=str)

    user_args = parser.parse_args()
    
    try:
        log_file = user_args.log_file
    except AttributeError:
        log_file = DEFAULT_LOG_FILE
    logging.basicConfig(filename=log_file, level=logging.INFO)
    
    if user_args.setup is not None:
        utils.logMessage('Setup requested in directory: ' + user_args.setup)
        import setup
        setup.main(user_args.setup)
        exit()

    else:
        configuration = read_config.read_xml(user_args.xml_config_file)
        utils.logMessage('read configuration file: ' + user_args.xml_config_file)
    
        watcher = pvwatch.PvWatch(configuration)
    
        utils.logMessage('starting the monitor and report cycle')
        watcher.start()


if __name__ == '__main__':
    '''call the command-line interface'''
    main()
