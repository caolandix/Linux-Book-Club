import urllib2
import socket
import time
from collections import defaultdict
from concurrent import futures

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
    print "The top five disallowed are: "
    print sorted(map_disallow, key=map_disallow.get, reverse=True)[:5]
    print "The top five user-agents are: "
    print sorted(map_user_agents, key=map_user_agents.get, reverse=True)[:5]

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
    return sorted([item.strip() for item in content])

"""
Function Name: build_maps
Purpose: Loops through the domains downloading the robots.txt file for each the builds the dicts needed
Inputs:
    - domain_list: the sorted list of domain names
Outputs:
    - disallow_map and useragent_map as dictionaries markign the number of times one of them occurred
Notes: 
"""
def build_maps(domain_list):
    disallow_map = defaultdict(int)
    useragent_map = defaultdict(int)
    robots_file = "robots.txt"
    
    print "Reading domain list..."
    
    with futures.ThreadPoolExecutor(max_workers = 5) as executor:
        tmp_disallow_map = defaultdict(int)
        tmp_useragent_map = defaultdict(int)
        for domain in domain_list:
            
            print "Processing http://%s/%s" % (domain, robots_file)
            executor.submit(process_robots_file, domain, tmp_disallow_map, tmp_useragent_map)
            
            # merge the tmp maps with the main
            for key in tmp_disallow_map:
                if key not in disallow_map.keys():
                    disallow_map[key] = tmp_disallow_map[key]
                else:
                    disallow_map[key] += tmp_disallow_map[key]
            for key in tmp_useragent_map:
                if key not in useragent_map.keys():
                    useragent_map[key] = tmp_useragent_map[key]
                else:
                    useragent_map[key] += tmp_useragent_map[key]
            tmp_disallow_map = defaultdict(int)
            tmp_useragent_map = defaultdict(int)
    return (disallow_map, useragent_map)

"""
Function Name: process_robots_file
Purpose: The thread function used in build_maps() that downloads the robots.txt file and then scans through it putting the user-agent and disallow strings into the associated dictionaries
Inputs:
    - domain: the domain being worked on
    - disallow_map: disallow_map
    - useragent_map: useragent_map
Outputs: n/a
Notes: 
"""
def process_robots_file(domain, disallow_map, useragent_map):
    robots_file = "robots.txt"
    download_file(domain, robots_file)
    with open(robots_file) as f:
        content = f.readlines()
    robots_lines = [item.strip() for item in content]
    for line in robots_lines:
        if "user-agent: " in line.lower():
            if line not in useragent_map.keys():
                useragent_map[line] = 1
            else:
                useragent_map[line] += 1
        elif "disallow: " in line.lower():
            if line not in disallow_map.keys():
                disallow_map[line] = 1
            else:
                disallow_map[line] += 1

"""
Function Name: run
Purpose: execution happens in this scope
Inputs: n/a
Outputs: n/a
Notes: 
"""    
def run():
    url_top_domains = "raw.githubusercontent.com/opendns/public-domain-lists/master"
    file_top_domains = "opendns-top-domains.txt"
    
    # download the domain file and load into a list
    download_file(url_top_domains, file_top_domains)
    domains = read_domainlist_into_list(file_top_domains)
    
    start_time = time.time()
    (disallow, user_agents) = build_maps(domains)
    end_time = time.time()
    
    print "Total time it took for execution: %sm" % str((end_time - start_time) / 60)
    
    # Output the top items
    output_top_five(disallow, user_agents)
    
    
if __name__ == '__main__':
    run()