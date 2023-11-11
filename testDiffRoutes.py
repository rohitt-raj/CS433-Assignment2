from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController # from http://installfights.blogspot.com/2016/12/exception-could-not-find-default.html


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"
    # required topology

    # pylint: disable=arguments-differ
    def build( self, **_opts ):
        # create the routers for each subnet (sets IP at eth1)
        ra = self.addNode('ra', cls=LinuxRouter, ip="192.168.1.1/24")
        rb = self.addNode('rb', cls=LinuxRouter, ip="172.16.0.1/12")
        rc = self.addNode('rc', cls=LinuxRouter, ip="10.0.0.1/8")

        # create switches for each subnet
        s12, s34, s56 = [ self.addSwitch(s) for s in ( 's12', 's34', 's56' ) ]

        # link switches to the routers
        self.addLink( s12, ra, intfName2="ra-eth1", params2={ 'ip' : "192.168.1.1/24" } ) 
        self.addLink( s34, rb, intfName2="rb-eth1", params2={ 'ip' : "172.16.0.1/12" } )
        self.addLink( s56, rc, intfName2="rc-eth1", params2={ 'ip' : "10.0.0.1/8" } )

        # create hosts
        h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='192.168.1.101/24', defaultRoute='via 192.168.1.1' )

        h3 = self.addHost( 'h3', ip='172.16.0.100/12', defaultRoute='via 172.16.0.1' )
        h4 = self.addHost( 'h4', ip='172.16.0.101/12', defaultRoute='via 172.16.0.1' )

        h5 = self.addHost( 'h5', ip='10.0.0.100/8', defaultRoute='via 10.0.0.1' )
        h6 = self.addHost( 'h6', ip='10.0.0.101/8', defaultRoute='via 10.0.0.1' )

        # link hosts to switches in each subnet
        for h, s in [(h1,s12), (h2,s12), (h3,s34), (h4,s34), (h5,s56), (h6,s56)]:
            self.addLink( h, s )


        # connect routers
        self.addLink(ra,
                     rb,
                     intfName1='ra-eth2',
                     intfName2='rb-eth3',
                     params1={'ip': '10.100.0.1/24'}, 
                     params2={'ip': '10.100.0.2/24'}) 

        self.addLink(rb,
                     rc,
                     intfName1='rb-eth2',
                     intfName2='rc-eth3',
                     params1={'ip': '10.100.1.1/24'},
                     params2={'ip': '10.100.1.2/24'}) 

        self.addLink(rc,
                     ra,
                     intfName1='rc-eth2',
                     intfName2='ra-eth3',
                     params1={'ip': '10.100.2.1/24'},
                     params2={'ip': '10.100.2.2/24'}) 

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo,
                   waitConnected=True)  

    # Add routing for reaching networks that aren't directly connected
    # ra <-> rc
    #info(net['ra'].cmd("ip route add 10.0.0.0/8 via 10.100.2.1 dev ra-eth3"))
    net['ra'].cmd("ip route add 10.0.0.0/8 via 10.100.1.2 dev ra-eth2") # new route for ra to rc: ra->rb->rc
    net['rc'].cmd("ip route add 192.168.1.0/24 via 10.100.0.1 dev rc-eth3")

    # ra <-> rb
    net['ra'].cmd("ip route add 172.16.0.0/12 via 10.100.0.2 dev ra-eth2")
    net['rb'].cmd("ip route add 192.168.1.0/24 via 10.100.0.1 dev rb-eth3")

    # rb <-> rc
    net['rb'].cmd("ip route add 10.0.0.0/8 via 10.100.1.2 dev rb-eth2")
    net['rc'].cmd("ip route add 172.16.0.0/12 via 10.100.1.1 dev rc-eth3")

    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
