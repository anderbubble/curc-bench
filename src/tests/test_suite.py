"""Automated test suite for curc-bench"""
import unittest
import re
import pyslurm
import os
import subprocess

from create import free_SLURM_nodes
from create import reservations
from hostlist import expand_hostlist


class MyTest(unittest.TestCase):
    """Test cases for curc-bench"""
    def test(self):
        """An unimportant test"""
        self.assertEqual(1, 1)

    def test_free_SLURM_nodes(self):
        """Test the functionalisty of pyslurm compared to subprocess.Popen commands"""

        #Old code using subprocess.Popen

        old_all_nodes = expand_hostlist("node[01-17][01-80]")
        free_nodes = free_SLURM_nodes("node[01-17][01-80]")
        reserved_nodes = reservations()

        diff_set = set(free_nodes).difference(set(reserved_nodes))
        node_list = []
        for node in diff_set:
            node_list.append(node)

        #New code using pyslurm
        a = pyslurm.node()
        node_dict = a.get()
        slurm_free_nodes = []
        all_nodes = []
        #if len(node_dict) > 0:
        ii = 0
        print "-" * 80
        for key, value in node_dict.iteritems():
            if key[0:4] == 'node': 
                all_nodes.append(key)
            #if ii > 150:
            #    break
            #ii += 3
            #print "%s :" % (key)
            #if key == 'node0149' or key == 'node1428':
               # print ''
            for part_key in sorted(value.iterkeys()):
                #if key == 'node0149' or key == 'node1428':
                   # print "\t%-15s : %s" % (part_key, value[part_key])
                #print "\t%-15s : %s" % (part_key, value[part_key])
                if part_key == 'node_state':
                    #print "%s :" % (key), "    node_state = ",value[part_key]
                    if value[part_key] == 'IDLE' or value[part_key] == 'ALLOCATED':
                        if key[0:4] == 'node':
                            if int(key[4:6])>=01 and int(key[4:6])<=17:
                                if int(key[6:8])>=01 and int(key[6:8])<=80:
                                    slurm_free_nodes.append(key)

        b=pyslurm.reservation()
        reserve_dict=b.get()
        slurm_reserve_nodes=[]
        ii = 0
        print "-" * 80
        for key, value in reserve_dict.iteritems():
            print "%s :" % (key)
            i+=1
            for part_key in sorted(value.iterkeys()):
                print "\t%-15s : %s" % (part_key, value[part_key])
            if i>3:
                break

        print "Old total nodes found = ", len(old_all_nodes)        
        print "Free nodes in old code = ", len(node_list)
        print "Total nodes found = ", len(all_nodes)                            
        print "Number of slurm free nodes = ",len(slurm_free_nodes)
        
        diff_set = set(slurm_free_nodes).difference(set(node_list))
        print "First 10 on diff_list = ",list(diff_set)[0:10]
        
        same_set = set(slurm_free_nodes).intersection(set(node_list))
        print "First 10 on same_list = ",list(same_set)[0:10]

        self.assertEqual(len(old_all_nodes),len(all_nodes))
        #self.assertEqual(node_list, slurm_free_nodes)
                #else:
                #    print "key = ",part_key
            #print "-" * 80

        # #else:
        # #    print "No Nodes found !"
        # print ''
        # print "Number of slurm free nodes = ",len(slurm_free_nodes)
        # #for nn in slurm_free_nodes:
        # #    print nn


if __name__ == '__main__':
    unittest.main()
