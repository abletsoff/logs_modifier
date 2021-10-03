# logs_obfuscator
Script for removing confidential information from events logs before sending them to technical support

# Functionality
<pre> 
positional arguments:
  FILE                  file for obfuscation

optional arguments:
    -h, --help            show this help message and exit
    -m, --mac             obfuscate MAC addresses
    -4, --ipv4            obfuscate IPv4 addresses
    -6, --ipv6            obfuscate IPv6 addresses
    -H, --hash            obfuscate salted hashes
    -p, --print           print result to stdout
    -r REGEX, --regex     REGEX 
                          user defined regex to obfuscate
    -P PASS_REGEX, --pass_regex PASS_REGEX 
                          user defined regex to not obfuscate 
</pre>

# PoC

<pre>
  ifconfig > ifconfig.log
  python3 logs_obfuscator.py -4 -m ifconfig.log
  vimdiff ifconfig.log ifconfig.log.obfuscated 
</pre>
# Screenshot
![alt text](https://github.com/abletsoff/logs_obfuscator/blob/main/PoC.png?raw=true)
