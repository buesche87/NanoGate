#!/bin/sh
echo "Content-type: text/html\n"

# read in our parameters
curip=$(ip a | grep "eth0" | egrep "inet" | awk '{ print $2 }' | cut -f1 -d"/")
curgw=$(sudo ip route | grep default | egrep eth0 | awk '{printf $3}')

# read in our parameters
CMD=`echo "$QUERY_STRING" | sed -n 's/^.*cmd=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
IP=`echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
GATEWAY=`echo "$QUERY_STRING" | sed -n 's/^.*gateway=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
PSK=`echo "$QUERY_STRING" | sed -n 's/^.*psk=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"| sed "s/%2F/\//g"`
IFACE=`echo "$QUERY_STRING" | sed -n 's/^.*iface=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

# our html header
echo "<html>"
echo "<head><meta name='viewport' content='width=device-width, initial-scale=1' /><title>NanoGate Settings</title> <link rel='stylesheet' type='text/css' href='style.css'></head>"
echo "<body>"
echo "<div style='text-align: center;'>"
echo "<div style='display: inline-block; text-align: left;'>"
 
if [ $CMD ]
then
  case "$CMD" in

    Send+Settings)
      echo "<center>Change IP to $IP/24<hr></center><pre>"
	  sudo chgip -set "$IP" "$GATEWAY" "$IFACE"> /dev/null 2>&1
      echo "</pre>"
	  echo "<meta http-equiv='refresh' content=';url=http://nanonagteway.nano.lan/'>"
    ;;

    Show+Settings)
	  echo "<center>Network Settings<hr></center><pre>"
      sudo chgip
      echo "</pre>"
    ;;

    Set+DHCP)
	  echo "<center>Change to DHCP Client<hr></center><pre>"
      sudo chgip -DHCP
      echo "</pre>"
    ;;

    Show+DHCP+Leases)
      echo "<center>DHCP Leases<hr></center><pre>"
      python3 /usr/local/nanogate/ldhcp.py
      echo "</pre>"
    ;;

    Change+Wifi+Key)
      echo "<center>Wifi Key<hr></center><pre>"
      sudo pskc "$PSK"
      echo "</pre>"
    ;;

    Send+UPnP)
      echo "<center>UPnP Message sent...<hr></center><pre>"
      upnps
      echo "</pre>"
    ;;
	
	Reboot)
      echo "<center>Reboot...</center>"
      sudo systemctl reboot
      echo "</pre>"
    ;;
	
	Shutdown)
      echo "<center>Shutdown...</center>"
      sudo shutdown -h now
    ;;

     *)
       echo "<center>Unknown command $CMD<br></center>"
       ;;
      esac
    fi
	
	echo "</div>"
	echo "<hr>"
	echo "</div>"


    # print out the form

    # page body
    
	echo "<center>"
	echo "NanoGate Network Settings"
	echo "<p>"

    echo "<form method=get>"
    echo "<table cellpadding='3'>"
    echo "<tbody>"
    echo "<tr>"
    echo "<td>eth0 IP:</td>"
    echo "<td width='30' padding:3px><input size='15' style='background-color: #fff4bd; color: black;' type=text name=ip onfocus=this.value='' value=$curip></td>"
    echo "</tr>"
	echo "<tr>"
	echo "<td>Gateway:</td>"
	echo "<td width='30' padding:3px><input size='15' style='background-color: #fff4bd; color: black;' type=text name=gateway onfocus=this.value='' value=$curgw></td>"
	echo "</tr>"
    echo "</tbody>"
    echo "</table>"
    echo "<p>"
 	echo "Access from VPN to"
	echo "<p>"
	echo "<input type=radio style='width: 14px; height: 14px;' name=iface value='wlan0' checked><label> WLAN</label>"
	echo "<input type=radio style='width: 14px; height: 14px;' name=iface value='eth0'><label> LAN</label>"
	echo "<p>"
	echo "<input type=submit name=cmd style='background-color: #ffbdbd; color: black;' value='Send Settings'>"
	echo "<input type=submit name=cmd style='background-color: #c0fcb1; color: black;' value='Show Settings'>"
	echo "<input type=submit name=cmd style='background-color: #fff4bd; color: black;' value='Set DHCP'>"
    echo "</form>"
    echo "<hr>"

	echo "DHCP Leases"
	echo "<p>"

    echo "<form method=get>"
    echo "<input type=submit name=cmd style='width:150px; background-color: #c0fcb1; color: black;' value='Show DHCP Leases'>"
	echo "</form>"	
    echo "<hr>"

    echo "Change NanoGateway Wifi Key"
    echo "<p>"

    echo "<form method=get>"
    echo "<input type=text name=psk style='width:150px; text-align:center;background-color: #fff4bd; color: black' required minlength='8' onfocus=this.value='' value='New_Wifi_Key'>"
    echo "<p>"
    echo "<input type=submit name=cmd style='width:150px; background-color: #ffbdbd; color: black;' value='Change Wifi Key'>"
    echo "</form>"
    echo "<hr>"

	echo "Download OpenVPN Profile"
	echo "<p>"

    echo "<form method=get action='/cgi-bin/NanoGate.ovpn'>"
    echo "<p>"
    echo "<input type=submit name=cmd style='background-color: #c0fcb1; color: black;' value='Download'>"
    echo "</form>"
    echo "<hr>"

	echo "pi-Hole Webinterface"
	echo "<p>"

    echo "<form method=get target='_blank' action='/admin'>"
    echo "<p>"
    echo "<input type=submit name=cmd style='background-color: #c0fcb1; color: black;' value='pi-Hole'>"
    echo "</form>"
    echo "<hr>"

	echo "Send UPnP Message"
	echo "<p>"

    echo "<form method=get>"
    echo "<p>"
    echo "<input type=submit name=cmd style='background-color: #c0fcb1; color: black;' value='Send UPnP'>"
    echo "</form>"
    echo "<hr>"
	
	echo "Power"
	echo "<p>"

    echo "<form method=get>"
    echo "<p>"
    echo "<input type=submit name=cmd style='background-color: #fff4bd; color: black;' value='Reboot'>"
    echo "<input type=submit name=cmd style='background-color: #ffbdbd; color: black;' value='Shutdown'>"
    echo "</form>"

	echo "</center>"
    echo "</body>"
    echo "</html>"

