hosts
=====

Short script to automate editing your hosts file

Usage
=====

I'm running the script locally on a Windows machine, running hosts.py from the location I've checked out the code with a batch script I've named `hosts.bat`:
```bat
@echo off
python C:\Users\[username]\Documents\GitHub\hosts\hosts.py %*
```

The rest of the documentation assumes you have the Python script aliased to a `hosts` command.

Lookup Hosts File Entry
-----------------------

Lookup the current IP address for a given host name, according to the hosts file:

    ~:$ hosts --get hostname
    hostname 192.168.1.1

Lookup the current IP address for any number of given host names, according to the hosts file:

    ~:$ hosts --get hostname1 hostname2 hostname3
    hostname1 192.168.1.13
    hostname2 192.168.1.14
    hostname3 192.168.1.15

Add a Hosts File Entry
----------------------

Set a host to resolve to a particular IP address (will overwrite your current hosts file with new contents):

    ~:$ hosts --set 192.168.1.10 hostname
    
    ~:$ hosts --get hostname
    hostname 192.168.1.10
    
Set any number of hosts to resolve to a particular IP address (will overwrite your current hosts file with new contents):

    ~:$ hosts --set 192.168.1.10 hostname1 hostname2 hostname3
    
    ~:$ hosts --get hostname1 hostname2 hostname3
    hostname1 192.168.1.10
    hostname2 192.168.1.10
    hostname3 192.168.1.10
    
Add a Hosts File Entry Based On Existing Entry
----------------------------------------------
    
Set a host to resolve to whatever IP address the hosts file resolves another host name to:
    
    ~:$ hosts --get hostname
    hostname 192.168.1.10

    ~:$ hosts --alias hostname hostname1
    
    ~:$ hosts --get hostname hostname1
    hostname 192.168.1.10
    hostname1 192.168.1.10
    
Other Notes
-----------

Any modifications to the hosts made by the script will completely overwrite the file. . I recommend backing it up before making substantial changes. 

Add the `--dry` option to any opertion that overwrites the hosts files to instead output the results to the screen without modifying the actual hosts file.