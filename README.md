hosts
=====

Short script to automate editing your hosts file

Usage
=====

Lookup the current IP address for a given host name, according to the hosts file:

    ~:$ python hosts.py --get hostname
    hostname 192.168.1.1

Lookup the current IP address for any number of given host names, according to the hosts file:

    ~:$ python hosts.py --get hostname1 hostname2 hostname3
    hostname1 192.168.1.13
    hostname2 192.168.1.14
    hostname3 192.168.1.15
    
Set a host to resolve to a particular IP address (will overwrite your current hosts file with new contents):

    ~:$ python hosts.py --set 192.168.1.10 hostname
    
    ~:$ python hosts.py --get hostname
    hostname 192.168.1.10
    
Set any number of hosts to resolve to a particular IP address (will overwrite your current hosts file with new contents):

    ~:$ python hosts.py --set 192.168.1.10 hostname1 hostname2 hostname3
    
    ~:$ python hosts.py --get hostname1 hostname2 hostname3
    hostname1 192.168.1.10
    hostname2 192.168.1.10
    hostname3 192.168.1.10
    
Set a host to resolve to whatever IP address the hosts file resolves another host name to:
    
    ~:$ python hosts.py --get hostname
    hostname 192.168.1.10

    ~:$ python hosts.py --alias hostname hostname1
    
    ~:$ python hosts.py --get hostname hostname1
    hostname 192.168.1.10
    hostname1 192.168.1.10

Any modifications to the hosts made by the script will completely overwrite the file. . I recommend backing it up before making substantial changes. 

Add the `--dry` option to any opertion that overwrites the hosts files to instead output the results to the screen without modifying the actual hosts file.