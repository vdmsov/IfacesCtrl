#!/usr/bin/python
import os
import subprocess
import time

class Routing:
    
    dev_if1 = "eth0"
    dev_if2 = "wlan0"
    dev_if3 = "ppp0"

    gw1 = "0.0.0.0"
    gw2 = "0.0.0.0"
    gw3 = "0.0.0.0"

    gw1_status = False
    gw2_status = False
    gw3_status = False

    max_lost = 50

    check_period = 20

#------------------------------------------------------------------------------

    def __init__(self):

        subprocess.Popen(["ifup " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
        subprocess.Popen(["pon sim2m"], stdout=subprocess.PIPE, shell = True)
        time.sleep(self.check_period)     

        process = subprocess.Popen(["ip route show | grep default |  grep " + self.dev_if1 + " | awk '{print $3}'"], stdout=subprocess.PIPE, shell = True)
        self.gw1 = process.communicate()[0]

        if os.path.exists("/sys/class/net/" + self.dev_if2) :
            process = subprocess.Popen(["ip route show | grep default |  grep " + self.dev_if2 + " | awk '{print $3}'"], stdout=subprocess.PIPE, shell = True)
            self.gw2 = process.communicate()[0]

        if os.path.exists("/sys/class/net/" + self.dev_if3) :
            process = subprocess.Popen(["""ifconfig """ + self.dev_if3 + """ | grep inet | grep P-t-P: | awk -F":" '{print $3}' | awk '{print $1}'"""], stdout=subprocess.PIPE, shell = True)
            self.gw3 = process.communicate()[0]

#------------------------------------------------------------------------------
    
    def get_current_status(self):

        subprocess.Popen(["ip r add 8.8.8.8 via " + self.gw1 + " dev " + self.dev_if1], stdout=subprocess.PIPE, shell = True)

        process = subprocess.Popen(["""ping -I """ + self.dev_if1 + """ -c5 -q -nW3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1"""], stdout=subprocess.PIPE, shell = True)
        gw1_curr_packet_loss = process.communicate()[0]

        subprocess.Popen(["ip r del 8.8.8.8 via " + self.gw1 + " dev " + self.dev_if1], stdout=subprocess.PIPE, shell = True)


        if (gw1_curr_packet_loss <= self.max_lost):
            self.gw1_status = True
            self.gw2_status = False
            self.gw3_status = False
        else:
            self.gw1_status = False

            subprocess.Popen(["ip r add 8.8.8.8 via " + self.gw2 + " dev " + self.dev_if2], stdout=subprocess.PIPE, shell = True)

            process = subprocess.Popen(["""ping -I """ + self.dev_if2 + """ -c5 -q -nW3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1"""], stdout=subprocess.PIPE, shell = True)
            gw2_curr_packet_loss = process.communicate()[0]
        
            subprocess.Popen(["ip r del 8.8.8.8 via " + self.gw2 + " dev " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
              
            if (gw2_curr_packet_loss <= self.max_lost):
                self.gw2_status = True
                self.gw3_status = False
            else:
                self.gw2_status = False
                subprocess.Popen(["ifdown " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
                subprocess.Popen(["ifup " + self.dev_if2], stdout=subprocess.PIPE, shell = True)

                subprocess.Popen(["ip r add 8.8.8.8 via " + self.gw3 + " dev " + self.dev_if3], stdout=subprocess.PIPE, shell = True)

                process = subprocess.Popen(["""ping -I """ + self.dev_if3 + """ -c5 -q -nW3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1"""], stdout=subprocess.PIPE, shell = True)
                gw3_curr_packet_loss = process.communicate()[0]
        
                subprocess.Popen(["ip r del 8.8.8.8 via " + self.gw3 + " dev " + self.dev_if3], stdout=subprocess.PIPE, shell = True)


                if (gw3_curr_packet_loss <= self.max_lost):
                    self.gw3_status = True
                else:
                    subprocess.Popen(["poff sim2m"], stdout=subprocess.PIPE, shell = True)
                    subprocess.Popen(["pon sim2m"], stdout=subprocess.PIPE, shell = True)

#------------------------------------------------------------------------------

    def switch_default_gw(self):

        if self.gw1_status:

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if3], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)

        if self.gw2_status:

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if1], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if3], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)

        if self.gw3_status:

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if1], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)

            process = subprocess.Popen(["ip route show | grep default | grep " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
            stdout = process.communicate()[0]
            print stdout
            if (len(stdout) > 3):
                subprocess.Popen(["ip route delete " + stdout], stdout=subprocess.PIPE, shell = True)


        process = subprocess.Popen(["""ip route show | grep -m1 default | awk '{print $3}'"""], stdout=subprocess.PIPE, shell = True)
        curr_gw = process.communicate()[0]


        if self.gw1_status:

            process = subprocess.Popen(["ip route show | grep default |  grep " + self.dev_if1 + " | awk '{print $3}'"], stdout=subprocess.PIPE, shell = True)
            self.gw1 = process.communicate()[0]

            if (curr_gw != self.gw1):
                if (len(curr_gw) < 3):
                    subprocess.Popen(["ip route add default via " + self.gw1 + " dev " + self.dev_if1], stdout=subprocess.PIPE, shell = True)
                else:
                    subprocess.Popen(["ip route replace default via " + self.gw1 + " dev " + self.dev_if1], stdout=subprocess.PIPE, shell = True)
                return

        else:

            if self.gw2_status:

                if (curr_gw != self.gw2):
                    if (len(curr_gw) < 3):
                        subprocess.Popen(["ip route add default via " + self.gw2 + " dev " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
                    else:
                        subprocess.Popen(["ip route replace default via " + self.gw2 + " dev " + self.dev_if2], stdout=subprocess.PIPE, shell = True)
                    return

            else:
                  
                if self.gw3_status:

                    process = subprocess.Popen(["""ifconfig """ + self.dev_if3 + """ | grep inet | grep P-t-P: | awk -F":" '{print $3}' | awk '{print $1}'"""], stdout=subprocess.PIPE, shell = True)
                    self.gw3 = process.communicate()[0]

                    if (len(curr_gw) < 3):
                        subprocess.Popen(["ip route add default via " + self.gw3 + " dev " + self.dev_if3], stdout=subprocess.PIPE, shell = True)
                        return

                    if (curr_gw != self.gw3):
                        if (len(curr_gw) < 3):
                            subprocess.Popen(["ip route add default via " + self.gw3 + " dev " + self.dev_if3], stdout=subprocess.PIPE, shell = True)
                        else:
                            subprocess.Popen(["ip route replace default via " + self.gw3 + " dev " + self.dev_if3], stdout=subprocess.PIPE, shell = True)
                        return

#------------------------------------------------------------------------------
