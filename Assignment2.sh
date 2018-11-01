#!/bin/bash
echo Author: Caolan O\'Domhnaill
echo 'Date: Mon Oct 29 14:55:47 PDT 2018'
echo "Assignment #2 - loads the robots.txt from many different domains and calculates some stats"
echo "The purpose of this script is to download the opendns top domains, and attempt to curl each of their robots.txt files."
echo "Then it finds the average robots.txt file, and output the top 5 user-agents and disallowed"
echo "Parameter #1 is the number of processor items that xargs uses to execute"

url_top_domains="https://raw.githubusercontent.com/opendns/public-domain-lists/master/opendns-top-domains.txt"
file_top_domains="opendns-top-domains.txt"

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

xargs -r -a ${file_top_domains} -d "\n" -P $1 -I{} ./script.sh {}

sleep 3s
echo "The Top 5 user Agents: "
cat user-agent.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -g | tail -n 5
echo "The Top Five Disallows: "
cat disallow.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -g | tail -n 5
