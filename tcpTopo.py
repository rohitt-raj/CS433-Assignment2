from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController # from http://installfights.blogspot.com/2016/12/exception-could-not-find-default.html

class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"
    # required topology

    # pylint: disable=arguments-differ
    def build( self, **_opts ):

        # create switches for each subnet
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        # create hosts
        h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 10.0.0.100') 
        h2 = self.addHost( 'h2', ip='192.168.1.101/24', defaultRoute='via 10.0.0.100' )
        h3 = self.addHost( 'h3', ip='172.16.0.100/12', defaultRoute='via 10.0.1.100' )
        h4 = self.addHost( 'h4', ip='172.16.0.101/12', defaultRoute='via 10.0.1.100' )


        # link hosts to switches and switches to each other
        for obj1, obj2 in [(h1,s1), (h2,s1), (h3,s2), (h4,s2), (s1,s2)]:
            self.addLink( obj1, obj2 ) 

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, waitConnected=True)  
    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
