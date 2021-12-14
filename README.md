# SDN Network Manager UI

## Prerequisite
  - Linux host with OpenDaylight Carbon [1] installed. The following packages should also be installed on ODL:
    - odl-restconf
    - odl-l2switch-switch
    - odl-dlux-*
  - Linux host with mininet [2] installed. It is best to install ODL and mininet on 2 different machines.
  - Linux host [3] with Python 3.6+

## Start the server
  1. Start ODL on [1]
     ```
     ./distribution-karaf-0.6.4-Carbon/bin/karaf
     ```
  2. Start mininet on [2] with the topo defined in the file `mininet/topo.py`
     ```
     sudo mn --controller=remote,ip=[odl-ip] --custom mininet/topo.py --topo topo --switch ovsk,protocols=OpenFlow13
     ```
  3. On [3], create venv and install dependencies
     ```
     cd server
     python3 -m venv venv
     source venv/bin/activate
     pip3 install -r requirements.txt
     ```
  4. Update your ODL's IP by changing the `BASE_URL` variable in `server/config.py`
  5. Start the server:
     ```
     cd ..
     ./run.sh
     ```

## User Guide
  1. On first connect, the flows are filled automatically by the switches' self-learning capability. To add our own flows, we need to delete the flows created by the switches first. Go to Configuration > Delete flows
   
  2. We can manually add flows for each switch
   
  3. We can also just define the path, and the server will then manage the creation of the flows for us.
   
      * Using Dijkstra: provide the source and the destination hosts. Then, the server will automatically find a path connecting between the 2 hosts and create the corresponding flows on all switches.
  
      * Using custom path: we need to define the exact path from the source host to the destination host. The server will then add the necessary flows to the switches.