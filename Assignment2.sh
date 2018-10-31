#!/bin/bash
echo Author: Caolan O\'Domhnaill
echo 'Date: Mon Oct 29 14:55:47 PDT 2018'
echo "Assignment #2 - loads the robots.txt from many different domains and calculates some stats"
echo "The purpose of this script is to download the opendns top domains, and attempt to curl each of their robots.txt files."
echo "Then it finds the average robots.txt file, and output the top 5 user-agents and disallowed"

url_top_domains="https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-top-domains.txt"
file_top_domains="opendns-top-domains.txt"
file_size_sum=0
num_usable_domain_files=0

list_of_outputs=("user-agent.txt" "disallow.txt")

for file in "${list_of_outputs[@]}"
do
    # clean up output files
    if [ -f "./${file}" ]
    then
        rm -rf ${file}
    fi
done

echo "cURLing the file ${url_top_domains}"
curl -o ${file_top_domains} -L --connect-timeout 60 ${url_top_domains}

domain_count=0

echo "Looping through the contents of the file ${file_top_domains}"
for domain in $( cat ${file_top_domains} ); do
    
    full_robots_url="${domain}/robots.txt"

    echo "Downloading the robots.txt from the domain ${domain}"
    curl -o robots.txt -L --connect-timeout 60 "${full_robots_url}" 

    curl_result=$?
    if test ${curl_result} != "0"
    then
        echo "unable to download from ${domain}. Skipping..."
        continue
    fi
    
    # if file exists and is not empty
    echo "Checking to see if the robots.txt exists and is larger than 0 bytes"
    if [ -f "robots.txt" ] && [ -s "robots.txt" ]
    then
        echo "getting the size of the robots.txt file..."
        size=$(ls -l robots.txt | tr -s ' ' ',' | cut -d',' -f 6)
        
        if [ "$size" -gt "0" ]
        then
            num_usable_domain_files=$((num_usable_domain_files+1))
        fi
        file_size_sum=$((file_size_sum+size))
        
        echo "Appending robots.txt to the resultant file"
        grep -i "user-agent" robots.txt >> user-agent.txt
        grep -i "disallow" robots.txt >> disallow.txt
    else
        echo "robots.txt is empty for domain ${domain}"
    fi
    
    # for testing purposes: limit the number of domains processed
    domain_count=$((domain_count+1))
    
    if [ "${domain_count}" -gt "50" ]
    then
        break
    fi
done

# Generate the average file size of robots.txt
avg=$((file_size_sum/num_usable_domain_files))

echo "Average File Size: ${avg}"
echo "The Top 5 user Agents: "
cat user-agent.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -zn | tail -n 6
echo "The Top Five Disallows: "
cat disallow.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -zn | tail -n 6
return 0