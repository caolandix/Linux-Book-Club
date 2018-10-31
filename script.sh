#!/bin/bash 

full_robots_url="$1/robots.txt"

echo "Downloading the robots.txt from the domain ${domain}"
echo ${full_robots_url}
curl -o robots.txt -L --connect-timeout 5 ${full_robots_url}

echo "Appending robots.txt to the resultant file"
grep -i "user-agent" robots.txt >> user-agent.txt
grep -i "disallow" robots.txt >> disallow.txt