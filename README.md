## CS 433: Computer Networks (2023)

ASSIGNMENT 2
Animesh Tumne - 21110227
Rohit Raj - 21110179
=================================

### PART 1 (Mininet Implementation)

**Implementation:**

After saving the python script for the topology, open the terminal and follow the steps:
1. Run the python script: sudo python myNet.py
2. Write this command on mininet console and press enter: h3 tcpdump -n -i h3-eth0
3. Open xterm for h1 from mininet console: xterm h1
4. In the xterm window: ping -c 3 172.16.0.100

where, 172.16.0.100 is the IP addr for h3

**Observation:**

1. On mininet console: xterm ra
2. On xterm (ra) window: wireshark &
3. On mininet console: xterm h1
4. On xterm (h1) window: ping -c 3 172.16.0.100

which means h2 is pinged from h1 and packets travel via router 'ra' which is captured and shown on wireshark
Results are shown in write-up.

**Vary the default routing:**

We tries changing route for h1 to h6 by changing the ra and rc connections, but it didn't work (Destination not reachable). 
You may check the code in the file: testDiffRoutes.py

**Dump the routing tables:**

To obtain the routing table for router 'ra', command to be run on mininet console: ra ip route

=================================
