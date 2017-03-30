#!/usr/bin/python2.7

import argparse
import os
import sys
import subprocess
import json
import logging
from logging.handlers import RotatingFileHandler
import pdb


class deployment:

    def __init__(self, pipe_open, info_loger, info_json):

        self.pipeopen = pipe_open

        self.infologer = info_loger

        self.infojson = info_json

        self.logging_init()

    def command_init(self):

        parser = argparse.ArgumentParser(description='Process some integers.')

        parser.add_argument(
            "--deployment",
            action="store_true",
            help='Deploy New Openstack environment.',
            default='True')

        parser.add_argument(
            "--dir",
            help='select directory to which store fuel configure files.',
            default='./')

        self.args = parser.parse_args()

        self.path = self.args.dir

        return self.args

    def logging_init(self):

        Rthandler = RotatingFileHandler(
            'myapp.log', maxBytes=10 * 1024 * 1024, backupCount=10)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s: %(message)s')
        Rthandler.setFormatter(formatter)
        logging.getLogger('').addHandler(Rthandler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s: %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def get_node_info(self):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel2',
                                    'node',
                                    'list',
                                    '-f',
                                    'json'],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel2 not found or caused error')
            sys.exit(proc.returncode)

        nodeinfo = proc.communicate()

        self.nodeinfo_json = self.infojson.loads(nodeinfo[0])

        return self.nodeinfo_json

    def get_cluster_info(self):

        proc = self.pipeopen.Popen(
            ['timeout', '2', 'fuel2', 'node', 'list', '-f', 'json'], stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel2 not found or caused error')
            sys.exit(proc.returncode)

        nodeinfo = proc.communicate()

        self.nodeinfo_json = json.loads(nodeinfo[0])

    def get_node_num(self):

        self.node_num = len(self.nodeinfo_json)

    def store_node_id(self):

        self.id_list = []  # store node id

        for num in range(self.node_num):
            if self.nodeinfo_json[num]['status'] != 'ready':
                self.infologer.error('The original environment is not ready')
                sys.exit(1)

            self.id_list.append(str(self.nodeinfo_json[num]['id']))

    def get_env_num(self):

        self.cluster = self.nodeinfo_json[0]['cluster']

    def get_env_net_cfg_to_file(self):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel',
                                    '--env',
                                    str(self.cluster),
                                    'network',
                                    'download',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

    def get_env_setting_cfg_to_file(self):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel',
                                    '--env',
                                    str(self.cluster),
                                    'settings',
                                    'download',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

    def get_env_deploy_cfg_to_file(self):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel',
                                    '--env',
                                    str(self.cluster),
                                    'deployment',
                                    'default',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

    def get_node_cfg_to_file(self):

        id_list_idx = 0
        while id_list_idx < self.node_num:
            self.get_node_net_cfg_to_file(id_list_idx)
            self.get_node_attr_cfg_to_file(id_list_idx)
            self.get_node_disk_cfg_to_file(id_list_idx)
            id_list_idx += 1

        return id_list_idx

    def get_node_net_cfg_to_file(self, id_list_idx):

        proc = self.pipeopen.Popen(['tim'
                                    'eout',
                                    '2',
                                    'fuel',
                                    'node',
                                    '--node-id',
                                    self.id_list[id_list_idx],
                                    '--network',
                                    '--download',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

    def get_node_attr_cfg_to_file(self, id_list_idx):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel',
                                    'node',
                                    '--node-id',
                                    self.id_list[id_list_idx],
                                    '--attributes',
                                    '--download',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

    def get_node_disk_cfg_to_file(self, id_list_idx):

        proc = self.pipeopen.Popen(['timeout',
                                    '2',
                                    'fuel',
                                    'node',
                                    '--node-id',
                                    self.id_list[id_list_idx],
                                    '--disk',
                                    '--download',
                                    '--dir',
                                    self.path],
                                   stdout=self.pipeopen.PIPE)
        proc.wait()

        if proc.returncode != 0:
            self.infologer.error('command fuel not found or caused error')
            sys.exit(proc.returncode)

##############################auto_deploy main#############################


def deploy_main():

    deploy = deployment(subprocess, logging, json)

    args = deploy.command_init()

    if not os.path.isdir(args.dir):
        print "The path don't exist."
        sys.exit(1)

    if args.deployment:

        deploy.get_cluster_info()

        print args.deployment

    print args.dir
