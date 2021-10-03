import re
import sys
import argparse

#=== TODO: Add Salted hash regular expressions

def substitution(data, regex_str, name, excl_regex_str):
    
    regex = re.compile(regex_str)
    excl_regex = re.compile(excl_regex_str)

    match_values = re.finditer(regex, data)
    excl_values = re.finditer(excl_regex, data)
    
    dictionary = {}     # dictionary of values need to substitute
    indexed = {}        # same values - same index
   
    # Put all match values in to the dictionary
    for value in match_values:
        # value.group(0)    - matching string value
        # value.span()      - position in text where matching string is

        dictionary[value.span()] = value.group(0)
    
    # Exclude values from the dictionary
    for value in excl_values:
        excl_keys = []
        for key in dictionary.keys():
            value_range = range(key[0], key[1])
            if value.span()[0] in value_range or value.span()[1] in value_range:
                excl_keys.append(key)
        
        for key in excl_keys:
            dictionary.pop(key)

    # Substitute values
    for (left, right), value in dictionary.items():
        if value not in indexed:
            indexed[value] = str(len(indexed) + 1) 

        data = data[:left] + (name + '_' + indexed[value]).center(right - left, '*') + data[right:]

    return data

def arg_parser():
    
    parser = argparse.ArgumentParser(description=' CLI logs obfuscater '.center(50,'='))
    parser.add_argument('-m', '--mac', action='store_true', help='obfuscate MAC addresses')
    parser.add_argument('-4', '--ipv4', action='store_true', help='obfuscate IPv4 addresses')
    parser.add_argument('-6', '--ipv6', action='store_true', help='obfuscate IPv6 addresses')
    parser.add_argument('-H', '--hash', action='store_true', help='obfuscate salted hashes')
    parser.add_argument('-p', '--print', action='store_true', help='print result to stdout')
    parser.add_argument('-r', '--regex', action='store', help="user defined regex to obfuscate")
    parser.add_argument('-P', '--pass_regex', action='store', help="user defined regex to not obfuscate")

    parser.add_argument('files', metavar='FILE', type=str, nargs='+', help='file for obfuscation')

    return parser.parse_args()
    

# ============ Regular Expressions ====================

regex_MAC = (   r'(([0-9a-fA-F]{2}[:.]){5}'
                r'[0-9a-fA-F]{2})|'
                r'(([0-9a-fA-F]{4}[:.]){2}'
                r'[0-9a-fA-F]{4})')

#Exclude Broadcast MAC address from substitution
regex_MAC_excl = (  r'(([fF]{2}[:.]){5}'
                    r'[fF]{2})|'
                    r'(([fF]{4}[:.]){2}'
                    r'[fF]{4})')


regex_IPv4 = (  r'([1-2]?\d{1,2}\.){3}'
                r'[1-2]?\d{1,2}')

#Exclude Loopback, Broadcast addresses and Mostly masks
regex_IPv4_excl = ( r'(127\.0\.0\.1)|'
                    r'(255\.([1-2]?\d{1,2}\.){2}'
                    r'[1-2]?\d{1,2})')

# This is monster "https://ihateregex.io/expr/ipv6/"
regex_IPv6 = r'''(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'''

#Exclude Loopback
regex_IPv6_excl = r'::1'

regex_Salted_Hashes = ( r'\$2[abyx]\$\d\d\$.{53}') #bcrypt 

#====================================================

args = arg_parser()

for file_name in args.files:
  
    try:
        f = open(file_name)
        data = f.read()
        f.close()
    except FileNotFoundError as excp:
        print(excp)
        exit()

    except IsADirectoryError as excp:
        print(excp)
        exit()

    except PermissionError as excp:
        print(excp)
        exit()
    
    if args.pass_regex == None:
        args.pass_regex = r'$a'

    if args.mac == True: 
        data = substitution(data, regex_MAC, 'MAC', r'(' + regex_MAC_excl + r')|(' + args.pass_regex + r')') 
    if args.ipv4 == True: 
        data = substitution(data, regex_IPv4, 'IPv4', r'(' + regex_IPv4_excl + r')|(' + args.pass_regex + r')') 
    if args.ipv6 == True: 
        data = substitution(data, regex_IPv6, 'IPv6', r'(' + regex_IPv6_excl + r')|(' + args.pass_regex + r')') 
    if args.hash == True: 
        data = substitution(data, regex_Salted_Hashes, 'Salted_Hash', args.pass_regex) 
    if args.regex != None:
        data = substitution(data, args.regex, 'U', args.pass_regex)
    if args.print == True:
        print(data)

    f = open(file_name + '.obfuscated', "w")
    f.write(data)
    f.close
