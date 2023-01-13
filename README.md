# Detector
The Detector is a custom tool, implemented using Python and Scapy (Python tool to manipulate network packets), that is designed to determine whether a TCP SYN or a UDP Flood, Denial of Service attack is detected, given a packet capture (pcap) file as input. It was developed as part of my thesis project for my degree of Bachelor of Science in Informatics of the Athens University of Economics and Business (AUEB).

In the following section its functioning will be presented in greater detail as well as a simple guide for its use, that will include some use cases on the testing on the given pcap files.

The attempt was to build a tool that efficiently detects DoS attacks whilst keeping it simple, lightweight and rather fast. The flowchart provided in the pdf file, shows the simple format adopted for its implementation. The detection of a possible attack is based on rules, as in the Snort IDS.

Its execution requires two to four arguments as input - namely filename, destinationIP, count and interval - in order for the detection rule to be created. The counters for both TCP SYN and UDP packets are nullified and this fact also signals the beginning of the examination of the first interval. Inside this interval - which is a time period in which excessive packet rate would trigger an alert - the number of the TCP SYN and UDP packets are counted with the use of Scapy, a tool that helps recognize the type of each packet, among others. To keep the procedure simple, only the packet's type and destination IP are taken into consideration and no other parameter is examined. At the end of each packet's examination, the next packet of the current interval - if it exists - is checked. When an interval finishes, the counters of the TCP SYN and UDP packets are compared to the count variable set by the user - or the default one - and the Detector delivers a verdict about whether an attack was detected during this interval or not. A positive answer to that would trigger one or both of the TCP SYN and UDP alerts and then exit the program, whereas a negative one would continue the process with the next interval. 

The whole process finishes when one of the following two conditions is fulfilled. The first is the detection of an attack and the second one is reaching the end of the pcap file without detecting any attack. In both cases, the Detector will throw a message to the command line according to its findings.

Due to the testing and evaluation phase included in the thesis, the Detector includes a parameter (line 13) to measure the execution time of the algorithm. The extra print function at the end of the program (line 80) displays this execution time on the command line.

The function used to load the pcap file in the memory is called PcapReader (line 47). It is used over rdpcap, as the latter loads the whole pcap file on the memory, which can be really demanding in memory resources. On the contrary, PcapReader only loads one packet at a time on the memory, in order to save resources. 

The snapshots provided next, constitute some of the Detector's use cases when used on the testing pcap files provided in this repository.

![alt text](https://github.com/PanosPappasInfo/Detector/blob/main/help.png?raw=true)
