#!/usr/bin/python2.7

import argparse
import os
import sys
import subprocess
import json
import logging
from logging.handlers import RotatingFileHandler
import pdb


def command_init():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--deployment", action="store_true", help='Deploy New Openstack environment.', default='True')

    parser.add_argument("--dir", help='select directory to which store fuel configure files.', default='./')

    args = parser.parse_args()

    return args

def logging_init():

    Rthandler = RotatingFileHandler('myapp.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    Rthandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger('').addHandler(Rthandler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def get_cluster_info(path, pipeopen, infologer):

    proc = pipeopen.Popen(['timeout', '2', 'fuel2', 'node', 'list', '-f', 'json'], stdout=pipeopen.PIPE)
    proc.wait()

    if proc.returncode != 0:
        infologer.error('command fuel2 not found or caused error')
        sys.exit(proc.returncode)

    nodeinfo = proc.communicate()

    nodeinfo_json = json.loads(nodeinfo[0])

    node_num = len(nodeinfo_json)

    id_list = []  # store node id

    for num in range(node_num):
        if nodeinfo_json[num]['status'] != 'ready':
            infologer.error('The original environment is not ready')
            sys.exit(1)

        id_list.append(str(nodeinfo_json[num]['id']))

    cluster = nodeinfo_json[0]['cluster']

    proc = pipeopen.Popen(['timeout', '2', 'fuel', '--env', str(cluster), 'network', 'download', '--dir', path], stdout=pipeopen.PIPE)
    proc.wait()

    if proc.returncode != 0:
        infologer.error('command fuel not found or caused error')
        sys.exit(proc.returncode)

    proc = pipeopen.Popen(['timeout', '2', 'fuel', '--env', str(cluster), 'settings', 'download', '--dir', path],
                            stdout=pipeopen.PIPE)
    proc.wait()

    if proc.returncode != 0:
        infologer.error('command fuel not found or caused error')
        sys.exit(proc.returncode)

    proc = pipeopen.Popen(['timeout', '2', 'fuel', '--env', str(cluster), 'deployment', 'default', '--dir', path],
                            stdout=pipeopen.PIPE)
    proc.wait()

    if proc.returncode != 0:
        infologer.error('command fuel not found or caused error')
        sys.exit(proc.returncode)

    proc = pipeopen.Popen(['timeout', '2', 'fuel', '--env', str(cluster), 'network', 'download', '--dir', path],
                            stdout=pipeopen.PIPE)
    proc.wait()

    if proc.returncode != 0:
        infologer.error('command fuel not found or caused error')
        sys.exit(proc.returncode)

    for id_list_idx in range(node_num):

        proc = pipeopen.Popen(['timeout', '2', 'fuel', 'node', '--node-id', id_list[id_list_idx], '--network', '--download', '--dir', path],
                                stdout=pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

        proc = pipeopen.Popen(
            ['timeout', '2', 'fuel', 'node', '--node-id', id_list[id_list_idx], '--attributes', '--download', '--dir', path],
            stdout=pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

        proc = pipeopen.Popen(
            ['timeout', '2', 'fuel', 'node', '--node-id', id_list[id_list_idx], '--disk', '--download', '--dir', path],
            stdout=pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)


    return nodeinfo_json

def deploy_main(cluster_info_json):
    pass


def load_env_cfg_main():
    pass

#################################################auto_deploy main#######################################################

args = command_init()

infologer = logging_init()

if not os.path.isdir(args.dir):
    print "The path don't exist."
    sys.exit(1)


if args.deployment:

    cluster_info_json = get_cluster_info(args.dir, subprocess, logging)

    deploy_main(cluster_info_json)

    print args.deployment

print args.dir





