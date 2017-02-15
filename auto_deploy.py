#!/usr/bin/python2.7

import argparse
import os
import sys
import subprocess
import json
import pdb

def get_cluster_info(path):

    proc = subprocess.Popen(['fuel2', 'node', 'list', '-f', 'json'], stdout=subprocess.PIPE)
    proc.wait()

    if proc.returncode != 0:
        print 'command fuel2 not found \n'
        sys.exit(proc.returncode)

    nodeinfo = proc.communicate()

    nodeinfo_json = json.loads(nodeinfo[0])

    node_num = len(nodeinfo_json)

    id_list = []  # store node id

    for num in range(node_num):
        if nodeinfo_json[num]['status'] != 'ready':
            print 'The original environment is not ready'
            sys.exit(1)

        id_list.append(str(nodeinfo_json[num]['id']))

    cluster = nodeinfo_json[0]['cluster']

    proc = subprocess.Popen(['fuel', '--env', str(cluster), 'network', 'download', '--dir', path], stdout=subprocess.PIPE)
    proc.wait()

    if proc.returncode != 0:
        print 'command fuel not found \n'
        sys.exit(proc.returncode)

    proc = subprocess.Popen(['fuel', '--env', str(cluster), 'settings', 'download', '--dir', path],
                            stdout=subprocess.PIPE)
    proc.wait()

    proc = subprocess.Popen(['fuel', '--env', str(cluster), 'deployment', 'default', '--dir', path],
                            stdout=subprocess.PIPE)
    proc.wait()

    proc = subprocess.Popen(['fuel', '--env', str(cluster), 'network', 'download', '--dir', path],
                            stdout=subprocess.PIPE)
    proc.wait()

    for id_list_idx in range(node_num):

        proc = subprocess.Popen(['fuel', 'node', '--node-id', id_list[id_list_idx], '--network', '--download', '--dir', path],
                                stdout=subprocess.PIPE)
        proc.wait()

        proc = subprocess.Popen(
            ['fuel', 'node', '--node-id', id_list[id_list_idx], '--attributes', '--download', '--dir', path],
            stdout=subprocess.PIPE)
        proc.wait()

        proc = subprocess.Popen(
            ['fuel', 'node', '--node-id', id_list[id_list_idx], '--disk', '--download', '--dir', path],
            stdout=subprocess.PIPE)
        proc.wait()

    return nodeinfo_json

def deploy_main(cluster_info_json):
    pass
    #proc = subprocess.Popen(['fuel2', 'node', 'list', '-f', 'json'], stdout=subprocess.PIPE)


# class FooAction(argparse.Action):
#      def __init__(self, option_strings, dest, nargs=None, **kwargs):
#          print 'gg \n'
#          super(FooAction, self).__init__(option_strings, dest, **kwargs)
#
#      def __call__(self, parser, namespace, values, option_string=None):
         #deploy_main()


def load_env_cfg_main():
    pass


class Deployment(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        #print 'gg \n'
        super(Deployment, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        #deploy_main()
        return 1

    def pr(self, yy):
        print self.dest

#class gy1:


# class FooAction(argparse.Action):
#     def __init__(self, option_strings, dest, nargs=None, **kwargs):
#         if nargs is not None:
#             raise ValueError("nargs not allowed")
#         super(FooAction, self).__init__(option_strings, dest, **kwargs)
#
#     def __call__(self, parser, namespace, values, option_string=None):
#         print '%r %r %r' % (namespace, values, option_string)
#             setattr(namespace, self.dest, values)

#x = Deployment("tt", dest = "hh")

#x.pr("ss\n")
parser = argparse.ArgumentParser(description='Process some integers.')

#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')

#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

#parser.add_argument("gg", action=FooAction)

parser.add_argument("--deployment", action="store_true", help='Deploy New Openstack environment.', default='True')

parser.add_argument("--dir", help='select directory to which store fuel configure files.', default='./')

#parser.add_argument("--node", help='select directory to which store fuel configure files.')
#
#parser.add_argument('-integ', '--gui')
#parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()

if not os.path.isdir(args.dir):
    print "The path don't exist."
    sys.exit()
#    print os.path.isdir(args.dir)

if args.deployment:

    cluster_info_json = get_cluster_info(args.dir)

    deploy_main(cluster_info_json)
    print args.deployment

print args.dir

##print args.accumulate(args.integers)



