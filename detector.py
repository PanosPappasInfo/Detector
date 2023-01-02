import scapy.all as scapy
from scapy.utils import PcapReader
import sys
import getopt
import time


def error_message():
    print("USAGE: python3 detector.py -f Filename -d DestinationIP -c Count -i Interval.\nFilename and DestinationIP arguments are mandatory!")
    raise SystemExit()

#USAGE: python3 detector.py -f filename -d destination -c count -i interval

start_time = time.time() #variable to keep track of the execution time

count = 15000        #optional argument that needs default value set
interval = 1         #optional argument that needs default value set

#-f and -d arguments are mandatory and have to be the first two arguments/-h is optional and if chosen it has to be the single argument used
if len(sys.argv) < 5:
    if sys.argv[1] == '-h':
        print("USAGE: python3 detector.py -f Filename -d DestinationIP -c Count -i Interval.")
        raise SystemExit()
    else:
        error_message()
elif sys.argv[1] == '-f' and sys.argv[3] == '-d':
    path = sys.argv[2]
    dst = sys.argv[4]
elif sys.argv[1] == '-d' and sys.argv[3] == '-f':
    dst = sys.argv[2]
    path = sys.argv[4]
else:
    error_message()

#-c and -i arguments are optional and have to be last in the execution command
opts, args = getopt.getopt(sys.argv[5:], "c:i:", ['count', 'interval'])
for opt, arg in opts:
    if opt == '-c':
        count = int(arg)
    if opt == '-i':
        interval = int(arg)

udpc = 0    #udp packet counter
tcpc = 0    #tcp packet counter
br = False  #attack detected
frst = True #first packet of the file

pp = PcapReader(path)  #PcapReader loads only one packet per instance on the memory

for packet in pp:                                       #iterate through every packet in the pcap
    if frst:
        beginning_time = packet.time                    #t0 from the beginning of packet capture
        current_interval = beginning_time + interval    #intervals are set depending on the interval variable's value
        frst = False
    if packet.time > current_interval:
        if udpc > count:
            print("Alert! Potential UDP DoS.")		
            br = True
        if tcpc > count:
            print("Alert! Potential TCP SYN DoS.")
            br = True
        if br:
            break
        #next interval, reset counters
        udpc = 0
        tcpc = 0
        current_interval += interval

    if packet.sprintf("%IP.dst%") == dst:                #count packets only if the destination IPs match
       if "TCP" in packet:                               #TCP packet?
           if packet.sprintf("%TCP.flags%") == 'S':        #SYN flag on?
               tcpc += 1                                      
       elif "UDP" in packet:                             #UDP packet?
           udpc += 1                                       

pp.close()


if not br:                                               #if no alert triggered
    print("No attacks were detected")


print("The execution time was: %s seconds." % (round((time.time() - start_time), 3)))   #total execution time output
