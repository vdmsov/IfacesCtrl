#!/bin/sh

#exit(0)
#LOG file
log="/var/log/routing.log"

#check period
# 1m, 10m, 1h

check_period="20s"

clear_log ()
{
if [ ! -f ${log} ];then
    touch ${log}
else
    cat /dev/null > ${log}
fi
}

init (){
 serial=`cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2`
 
 ifup wlan0
 pon sim2m
 sleep ${check_period}
 
 dev_if1="eth0"
 dev_if2="wlan0"
 dev_if3="ppp0"
 
 
 #ip1=`ifconfig ${dev_if1} | awk -F ' *|:' '/inet addr/{print $4}'`
 #ip2=`ifconfig ${dev_if2} | awk -F ' *|:' '/inet addr/{print $4}'`
 #ip3=`ifconfig ${dev_if3} | awk -F ' *|:' '/inet addr/{print $4}'`

 gw1=`ip route show | grep default | grep $dev_if1 | awk '{print $3}'`
 
 if [ -d /sys/class/net/wlan0 ]; then
  gw2=`ip route show | grep default | grep $dev_if2 | awk '{print $3}'`
 fi
 
 if [ -d /sys/class/net/ppp0 ]; then
  gw3=`ifconfig $dev_if3 | grep inet | grep P-t-P: | awk -F":" '{print $3}' | awk '{print $1}'`
 fi
  
 if [ ${#gw1} -lt 3 ]; then
        gw1="192.168.1.1"
 fi
 if [ ${#gw2} -lt 3 ]; then
        gw2="192.168.1.1"
 fi

 gw1_status=0
 gw2_status=0
 gw3_status=0

 max_lost=50

 #ip r add 8.8.8.8 via ${gw1} dev eth0
 #ip r add 8.8.8.8 via ${gw2} dev wlan0

 # set only one default GW in start!!!
# if [ `ip route show | grep default | wc -l` -gt 1 ]; then
#       str=`ip route show | grep default | grep wlan0`
#       ip route delete $str
# fi

clear_log
    echo `date +"%T %d.%m.%Y"`." Init environment OK. Check gateways status every ${check_period}." >> ${log}
    mosquitto_pub -h localhost -p 1883 -t "/xiot/wb${serial}/system/routing/mess/" -m "Init environment OK"
}

get_current_status () {
 ip r add 8.8.8.8 via ${gw1} dev eth0
 gw1_curr_packet_loss=`ping -I ${dev_if1} -c5 -q -W3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1`
 ip r del 8.8.8.8 via ${gw1} dev eth0
 if [ ${gw1_curr_packet_loss} -le ${max_lost} ]; then
        gw1_status=1
        gw2_status=0
        gw3_status=0
        echo `date +"%T %d.%m.%Y"`. "ISP1. [STATUS - OK]. Current packet loss on ${gw1} via ${dev_if1} is ${gw1_curr_packet_loss}%." >> ${log}
        #mosquitto_pub -h localhost -p 1883 -t "/xiot/wb${serial}/system/routing/" -m "ISP1 OK"
 else
        gw1_status=0
        echo `date +"%T %d.%m.%Y"`. "ISP1. [STATUS - CRITICAL]. Current packet loss on ${gw1} via ${dev_if1} is ${gw1_curr_packet_loss}%." >> ${log}
        #mosquitto_pub -h localhost -p 1883 -t "/xiot/wb${serial}/system/routing/" -m "ISP1 FAIL"
        
        ip r add 8.8.8.8 via ${gw2} dev wlan0
        gw2_curr_packet_loss=`ping -I ${dev_if2} -c5 -q -W3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1`
        ip r del 8.8.8.8 via ${gw2} dev wlan0
        
        if [ ${gw2_curr_packet_loss} -le ${max_lost} ]; then
                gw2_status=1
                gw3_status=0
                echo `date +"%T %d.%m.%Y"`. "ISP2. [STATUS - OK]. Current packet loss on ${gw2} via ${dev_if2} is ${gw2_curr_packet_loss}%." >> ${log}
                #mosquitto_pub -h localhost -p 1883 -t "/xiot/wb${serial}/system/routing/" -m "ISP2 OK"
        else
                gw2_status=0
                echo `date +"%T %d.%m.%Y"`. "ISP2. [STATUS - CRITICAL]. Current packet loss on ${gw2} via ${dev_if2} is ${gw2_curr_packet_loss}%." >> ${log}
                #mosquitto_pub -h localhost -p 1883 -t "/xiot/wb${serial}/system/routing/" -m "ISP2 FAIL"
                ifdown wlan0
                ifup wlan0
                
                 ip r add 8.8.8.8 via ${gw3} dev ppp0
                 gw3_curr_packet_loss=`ping -I ${dev_if3} -c5 -q -W3 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1`
                 ip r del 8.8.8.8 via ${gw3} dev ppp0
                 if [ ${gw3_curr_packet_loss} -le ${max_lost} ]; then
                    gw3_status=1
                 else
                    poff sim2m
                    pon sim2m
                 fi
        fi
 fi
}

switch_default_gw () {
        if [ $gw1_status -eq 1 ]; then
                str=`ip route show | grep default | grep wlan0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
                str=`ip route show | grep default | grep ppp0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
        fi
        if [ $gw2_status -eq 1 ]; then
                str=`ip route show | grep default | grep eth0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
                str=`ip route show | grep default | grep ppp0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
        fi
        if [ $gw3_status -eq 1 ]; then
                str=`ip route show | grep default | grep eth0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
                str=`ip route show | grep default | grep wlan0`
                if [ ${#str} -gt 3 ]; then
                        ip route delete $str
                fi
        fi


  curr_gw=`ip route show | grep -m1 default | awk '{print $3}'`
  echo "CUR - ${curr_gw}; st1- ${gw1_status}; st2 - ${gw2_status}; st3 - ${gw3_status}" >> ${log}
  ip route show >> ${log}


  if [ ${gw1_status} -eq 1 ]; then
        gw1=`ip route show | grep default | grep $dev_if1 | awk '{print $3}'`
        if [ ${curr_gw} = ${gw1} ]; then

        else
                if [ ${#curr_gw} -lt 3 ]; then
                 ip route add default via ${gw1} dev ${dev_if1}
                else
                 ip route replace default via ${gw1} dev ${dev_if1}
                fi
                return
        fi

  else
        if [ ${gw2_status} -eq 1 ]; then
                if [ ${curr_gw} = ${gw2} ]; then

                else
                        if [ ${#curr_gw} -lt 3 ]; then
                         ip route add default via ${gw2} dev ${dev_if2}
                        else
                         ip route replace default via ${gw2} dev ${dev_if2}
                        fi
                        return
                fi
        else
            if [ $gw3_status -eq 1 ]; then
                gw3=`ifconfig $dev_if3 | grep inet | grep P-t-P: | awk -F":" '{print $3}' | awk '{print $1}'`
                if [ ${#curr_gw} -lt 3 ]; then
                        ip route add default via ${gw3} dev ${dev_if3}
                        return
                fi
                if [ ${curr_gw} = ${gw3} ]; then

                else
                        if [ ${#curr_gw} -lt 3 ]; then
                         ip route add default via ${gw3} dev ${dev_if3}
                        else
                         ip route replace default via ${gw3} dev ${dev_if3}
                        fi

                        return
                fi
            fi
        fi
  fi

}

#init

# go in Loop without end

${gw1}

#while [ 1 ]
#do
#        get_current_status
#        switch_default_gw
#        sleep ${check_period}
#done