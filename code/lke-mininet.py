from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.node import OVSKernelSwitch
from mininet.node import OVSSwitch
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import waitListening
from mininet.log import lg, info
from mininet.node import Node

from functools import partial

import json
import time
import random
import threading

import time
import pandas as pd
import subprocess
import os

#import set_config as sc

class NewTopo( Topo ):
    """
    Builds a mininet topology based off the topology.json file
    Topo: the mininet object that holds the topology information
    """
    def build( self, config):
        switches = {} 
        hosts = {}
        links = {}

        # Create switches 
        for switch in config['switch_info']: 
            #switches[switch['switch_name']] = self.addSwitch(switch['switch_name'], datapath='user')
            switches[switch['switch_name']] = self.addSwitch(switch['switch_name'])

        # Create hosts 
        for host in config['host_info']:
            hosts[host['host_name']] = self.addHost( host['host_name'],
                    ip=host['ip_address'],
                    mac=host['mac_address'],
                    cpu=host['cpu'])

        # Create links 
        for link in config['link_info']:
            #self.addLink(hosts[link['source']], switches[link['destination']])
            self.addLink(hosts[link['source']], switches[link['destination']], 
                    bw=link['bw'], 
                    delay=link['delay'], 
                    loss=link['loss'], 
                    max_queue_size=link['max_queue_size'], use_htb=True)

        """
        for host in config['host_info']:
            hosts[host['host_name']] = self.addHost( host['host_name'],
                    ip=host['ip_address'],
                    mac=host['mac_address']
                    )
        for link in config['link_info']:
            #self.addLink(hosts[link['source']], switches[link['destination']])
            self.addLink(hosts[link['source']], switches[link['destination']], 
                    bw=10, 
                    delay='5ms', 
                    loss=2, 
                    max_queue_size=1000, use_htb=True)
        """

def connectToRootNS( network, switch, ip, routes ):
    """
    Connects hosts to root namespace via switch and starts the network.
    network: Mininet() network object
    switch: switch to connect to root namespace
    ip: IP address for root namespace node
    routes: host networks to route to
    """

    # Create a node in root namespace and link to switch 0
    root = Node('root', inNamespace=False)
    intf = network.addLink(root, switch).intf1
    root.setIP( ip, intf=intf )

    # Start network that now includes link to root namespace
    network.start()

    """
    # Setup userspace switch
    #ret = switches['ovs_1'].cmd('sudo ovs-vsctl set bridge ovs_1 protocols=OpenFlow13')
    ret = switch.cmd('sudo ovs-vsctl set bridge ovs_1 protocols=OpenFlow13')
    print(ret)
    #ret = switches['ovs_1'].cmd("sudo ovs-ofctl add-flow ovs_1 'priority=1 action=normal' -O OpenFlow13")
    ret = switch.cmd("sudo ovs-ofctl add-flow ovs_1 'priority=1 action=normal' -O OpenFlow13")
    print(ret)
    """

    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def sshd( network, cmd='/usr/sbin/sshd', opts='-D', ip='10.123.123.1/32', routes=None, switch=None ):
    """
    Launches sshd on all hosts in the given network
    ip: root-eth0 IP address in root namespace (10.123.123.1/32)
    routes: Mininet host networks to route to (10.0/24)
    switch: Mininet switch to connect to root namespace (s1)
    """

    if not switch:
        # Default switch if none is provided  
        switch = network['ovs_1']  
    if not routes:
        routes = [ '10.0.0.0/24' ]

    # Start the network and connect it to root ns
    connectToRootNS(network, switch, ip, routes)

    # Launch the sshd
    for host in network.hosts:
        ret = host.cmd(cmd + ' ' + opts + ' &')
        print(ret)

    info("*** Waiting for ssh daemons to start\n")
    for server in network.hosts:
        waitListening(server=server, port=22, timeout=5)

    info("\n*** Hosts are running sshd at the following addresses:\n")
    for host in network.hosts:
        info( host.name, host.IP(), '\n' )

    info("\n*** Type 'exit' or control-D to shut down network\n")

def startNetwork(config_path):
    
    # Configure various aspects of the Drawbridge system based on the drawbridge-topology file
    with open(config_path) as json_file:
        config = json.load(json_file)
    json_file.close()
    #sc.reconfig(config)

    # Dictionaries to hold and easily access mininet objects
    hosts = {}
    switches = {}
    controllers = {}

    # Use default mininet controller (POX) to set up the network
    # Add other drawbridge controllers to the topology
    topo = NewTopo(config)
    
    net = Mininet(topo=topo, link=TCLink, host=CPULimitedHost)

    for controller in config['controller_info']:
        controllers[controller['controller_name']] = net.addController(
                controller['controller_name'],
                controller=RemoteController,
                ip=controller['ip_address'],
                port=controller['port']
                )

    net.addNAT().configDefault()

    # Create network (network starts within) 
    # Start SSH demons on each host
    sshd(net, opts='-D -o UseDNS=no -u0', ip='10.0.2.15')

    for host in config['host_info']:
        hosts[host['host_name']] = net.get(host['host_name'])
    print(hosts)

    for switch in config['switch_info']:
        switches[switch['switch_name']] = net.get(switch['switch_name'])
    print(switches)

    # Test network capacity
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing network bandwidth")
    net.iperf((hosts['client'], hosts['server']))

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    config_path = '/vagrant/topology-config.json'
    startNetwork(config_path)
