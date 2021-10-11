# logs_obfuscator
Script for removing confidential information from events logs before sending them to technical support

# Functionality
<pre> 

positional arguments:
  FILE                  file for modification

optional arguments:
  -h, --help            show this help message and exit
  -m, --mac             modify MAC addresses
  -4, --ipv4            modify IPv4 addresses
  -6, --ipv6            modify IPv6 addresses
  -H, --hash            modify salted hashes
  -p, --print           print result to stdout
  -r REGEX, --regex REGEX
                        user defined regex to modify
  -P PASS_REGEX, --pass_regex PASS_REGEX
                        user defined regex to not modify
  -d, --detail          display information about modified values

</pre>

# PoC

<pre>
  ifconfig > ifconfig.log
  python3 logs_modifier.py -4 -m ifconfig.log
  vimdiff ifconfig.log ifconfig.log.modified 
</pre>
# Screenshot
![alt text](https://github.com/abletsoff/logs_modifier/blob/main/PoC.png?raw=true)
