#!/curc/admin/benchmarks/bin/python
import os, sys
from datetime import datetime
from optparse import OptionParser

appsdir = '/root/srv/www/benchmarks/apps/'
if not appsdir in sys.path:
    sys.path.insert(0,appsdir)

appsdir = '/root/srv/www/benchmarks/'
if not appsdir in sys.path:
    sys.path.insert(1,appsdir)

os.environ["DJANGO_SETTINGS_MODULE"] = "benchmarks_site.settings"
from django.db import models
from wire.models import Bandwidth
from django.db import IntegrityError

from bench.util import config
import logging
logger = logging.getLogger('Benchmarks')

def bandwidth_data(in_file):

    data_bandwidth = {'4194304':0,'1048576':0,'262144':0,'65536':0}
    while in_file:
        line = in_file.readline()
        #print line
        split = line.split()
        if not split:
            break
        if split[0] == '#':
            continue
        try:
            data_bandwidth[split[0]] = split[1]
        except IndexError:
            logger.error("missing linpack data")

    return data_bandwidth

def insert_bandwidth(data, subdirname, td, tr):
    node1 = subdirname[:8]
    node2 = subdirname[9:]
    tmp = datetime(year=td.year, month=td.month, day=td.day, hour=int(tr))

    bw = Bandwidth(test_date=tmp, name=node1, node1=node1, node2=node2, test1=data['65536'], test2=data['262144'], test3=data['1048576'], test4=data['4194304'], effective=True)
    try:
        bw.save()
    except IntegrityError as e:
        logger.error("Bandwidth import error: " + str(e))

def import_data(path, date, trial):
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            if subdirname.find("node") == 0:
                data_file = os.path.join(path,subdirname,"data_bw")
                #print subdirname
                if os.path.exists(data_file):
                    in_file = open(data_file,"r")

                    b = bandwidth_data(in_file)
                    insert_bandwidth(b,subdirname,date, trial)

                    in_file.close()

def evaluate_bandwidth_data(data, subdirname, bad_nodes, good_nodes):

    #data_bandwidth = {'4194304':0,'1048576':0,'262144':0,'65536':0}
    value = (1-float(config.bandwidth_limits['percent']/100.0))
    #print value
    node1 = subdirname[:8]
    node2 = subdirname[9:]

    # print float(data['4194304']),
    #    print float(data['1048576']),
    #    print float(data['262144']),
    #    print float(data['65536'])

    if float(data['4194304']) < float(config.bandwidth_limits['4194304']*value):
        data['4194304_effective'] = False
        bad_nodes.append(node1)
        bad_nodes.append(node2)
    else:
        data['4194304_effective'] = True
        good_nodes.append(node1)
        good_nodes.append(node2)

    if float(data['1048576']) < float(config.bandwidth_limits['1048576']*value):
        data['1048576_effective'] = False
        bad_nodes.append(node1)
        bad_nodes.append(node2)
    else:
        data['1048576_effective'] = True
        good_nodes.append(node1)
        good_nodes.append(node2)

    if float(data['262144']) < float(config.bandwidth_limits['262144']*value):
        data['262144_effective'] = False
        bad_nodes.append(node1)
        bad_nodes.append(node2)
    else:
        data['262144_effective'] = True
        good_nodes.append(node1)
        good_nodes.append(node2)

    if float(data['65536']) < float(config.bandwidth_limits['65536']*value):
        data['65536_effective'] = False
        bad_nodes.append(node1)
        bad_nodes.append(node2)
    else:
        data['65536_effective'] = True
        good_nodes.append(node1)
        good_nodes.append(node2)


def execute(dir_name, node_list):

    path = os.path.split(dir_name)
    trial = path[-1].split('-')[-1]
    year = path[-1].split('-')[0]
    month = path[-1].split('-')[1]
    day = path[-1].split('-')[2]

    node_path = os.path.join(dir_name,"bandwidth")
    logger.info(node_path)

    bad_nodes = []
    good_nodes = []
    for dirname, dirnames, filenames in os.walk(node_path):
        for subdirname in dirnames:
            #print subdirname
            if subdirname.find("node") == 0:
                data_file = os.path.join(node_path,subdirname,"data_bw")
                if os.path.exists(data_file):
                    in_file = open(os.path.join(node_path,subdirname,"data_bw"),"r")
                    b = bandwidth_data(in_file)
                    evaluate_bandwidth_data(b,subdirname,bad_nodes, good_nodes)

                    in_file.close()

    tested = set(good_nodes).union(set(bad_nodes))
    not_tested = set(node_list).difference(tested)

    return {'not_tested': list(not_tested), 'bad_nodes': list(set(bad_nodes)), 'good_nodes': list(set(good_nodes).difference(set(bad_nodes)))}