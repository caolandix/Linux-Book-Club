import urllib2
import socket
import time
from collections import defaultdict


"""
Function Name: download_file
Purpose: downloads a file and saves it to the same name
Inputs:
    - url: URL to where the file is on the net
    - filename: the file
Outputs: n/a
Notes: 
"""
def download_file(url, filename):
    num_attempts = 0
    max_attempts = 5
    f = None
    while num_attempts < max_attempts:
        try:
            full_url = "http://" + url + "/" + filename
            response = urllib2.urlopen(full_url, timeout = 5)
            content = response.read()
            f = open("./" + filename, 'w')
            f.write(content)
            f.close()
            break
        except socket.timeout as e:
            print type(e)
            print "There was an error: %r, on file: %s" % (e, full_url)
            break
        except urllib2.URLError as e:
            num_attempts += 1
        except Exception as e:
            break
        

"""
Function Name: output_top_five
Purpose: downloads a file and saves it to the same name
Inputs:
    - map_disallow: a map of the disallows and their counts
    - map_user_agents: a map of the user-agents and their counts
Outputs: n/a
Notes: 
"""    
def output_top_five(map_disallow, map_user_agents):
    sorted_disallowed = sorted(map_disallow.values())
    sorted_user_agents = sorted(map_user_agents.values())
    first5_disallowed = {i: sorted_disallowed[i] for i in sorted_disallowed.keys()[:5]}
    first5_user_agents = {i: sorted_user_agents[i] for i in sorted_user_agents.keys()[:5]}

    print "The top five disallowed are: "
    print sorted_disallowed.index

    print "The top five user-agents are: "
    print sorted_disallowed.index

"""
Function Name: read_domainlist_into_list
Purpose: Reads the domains into a list for iteration
Inputs:
    - filename: the name of the file to read in
Outputs:
    - a list of the domains
Notes: 
"""
def read_domainlist_into_list(filename):
    with open(filename) as f:
        content = f.readlines()
    return [item.strip() for item in content]

"""

"""
def build_maps(domain_list):
    disallow_map = defaultdict(int)
    useragent_map = defaultdict(int)
    robots_file = "robots.txt"
    
    print "Reading domain list..."
    for domain in domain_list:
        
        print "Processing http://%s/%s" % (domain, robots_file)
        download_file(domain, robots_file)
        with open(robots_file) as f:
            content = f.readlines()
        robots_lines = [item.strip() for item in content]
        for line in robots_lines:
            if "user-agent: " in line.lower():
                useragent_map[line] += 1
            elif "disallow: " in line.lower():
                disallow_map[line] += 1    
    return (disallow_map, useragent_map)

    
"""
Function Name: run
Purpose: execution happens in this scope
Inputs: n/a
Outputs: n/a
Notes: 
"""    
def run():

    robots_file = "robots.txt"
    url_top_domains = "raw.githubusercontent.com/opendns/public-domain-lists/master"
    file_top_domains = "opendns-top-domains.txt"
    
    # download the domain file and load into a list
    download_file(url_top_domains, file_top_domains)
    domains = read_domainlist_into_list(file_top_domains)
    
    start_time = time.time()
    (disallow, user_agents) = build_maps(domains)
    end_time = time.time()
    
    # Output the top items
    output_top_five(disallow, user_agents)
    
    
if __name__ == '__main__':
    run()