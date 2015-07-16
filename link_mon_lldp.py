# XXX que hacer cuando no hay pkts del tipo en un intervalo de tiempo?
# XXX por ejemplo LLDP en un switch cisco o CDP en uno switch no-cisco?
import os
import re
import subprocess

print "link_mon_lldp started"
lldp_pcap = '/tmp/lldp.pcap'

command = 'ip monitor link'
interface = 'eth0'
captured = False
status = subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          shell=True)

for line in iter(status.stdout.readline, b''):
    if re.search(interface, line):
        if re.search('DOWN', line):
            print "DOWN"
            captured = False
            if os.path.isfile(lldp_pcap):
                subprocess.call('sudo rm {}'.format(lldp_pcap), shell=True)
                print '{} deleted'.format(lldp_pcap)
        elif re.search('UP', line) and not captured:
            print "UP"
            cap_filter = '"ether proto 0x88cc"'
            sniff_cmd = "sudo tshark -i eth0 -c 1 -w {} -f {}".format(lldp_pcap, cap_filter)
            # entrar de promiscous manda up a ip monitor link
            # salir de promiscous manda up a monitor link
            # esto provocaba un loop hasta que se introdujo a "captured"
            subprocess.call(sniff_cmd, shell=True)
            command = "/bin/chmod 777 {}".format(lldp_pcap)
            subprocess.call(command, shell=True)
            print "tshark CDP done"
            captured = True
        else:
            print "UNKNOWN"
