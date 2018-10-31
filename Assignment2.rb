include 'rubygems'
include 'curb'
include 'FileTest'
require 'net/http'

require "open-uri"
require "fileutils"

def download(url, path)
  case io = open(url)
  when StringIO then File.open(path, 'w') { |f| f.write(io) }
  when Tempfile then io.close; FileUtils.mv(io.path, path)
  end
end

puts 'Author: Caolan O\'Domhnaill'
puts 'Date: Mon Oct 29 14:55:47 PDT 2018'
puts 'Assignment #2 - loads the robots.txt from many different domains and calculates some stats \
      The purpose of this script is to download the opendns top domains, and attempt to curl each of their robots.txt files.\
      Then it finds the average robots.txt file, and output the top 5 user-agents and disallowed'

url_top_domains = 'https://raw.githubusercontent.com'
path_to_domains_file = '/opendns/public-domain-lists/master/opendns-top-domains.txt'
top_domains_file = 'opendns-top-domains.txt'
file_size_col = 5
file_size_sum = 0
file_size_avg = 0
num_usable_domain_files = 0

list_of_outputs_files = [
  'user-agent.txt',
  'disallow.txt',
]

# remove the output files from the disk
for list_of_output_files.each do | filename |
  if File.file?(filename) then
    File.delete(filename)
  end
done

# Must be somedomain.net instead of somedomain.net/, otherwise, it will throw exception.
download(path_to_domains_file, top_domains_file)

File.open(file_top_domains).inject(0) { |num_domains, line| num_domains + 1 }

domain_count=0

puts "Looping through the contents of the file ${file_top_domains}"
for domain in $( cat ${file_top_domains} ); do
    
    full_robots_url = domain + String('/robots.txt')

    puts "Downloading the robots.txt from the domain ${domain}"
    curl -o robots.txt -L --connect-timeout 60 "${full_robots_url}"

    curl_result=$?
    if test ${curl_result} != "0"
    then
        puts "unable to download from ${domain}. Skipping..."
        continue
    fi
    
    # if file exists and is not empty
    puts "Checking to see if the robots.txt exists and is larger than 0 bytes"
        
    if File.file?('robots.txt') then
        puts "getting the size of the robots.txt file..."
        size = File.size('robots.txt')
        num_usable_domain_files += 1
        file_size_sum = file_size_sum + size
        
        grep -i "user-agent" robots.txt >> user-agent.txt
        grep -i "disallow" robots.txt >> disallow.txt
    else
        puts "robots.txt is empty for domain ${domain}"
    end
    
    # for testing purposes: limit the number of domains processed
    domain_count += 1
    
    if domain_count > 50 then
      break
    end
done

# Generate the average file size of robots.txt
avg = file_size_sum / num_usable_domain_files

puts "Average File Size: ${avg}"
puts "The Top Five user-agents: "
cat user-agent.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -zn | tail -n 6
puts "The Top Five Disallows: "
cat disallow.txt | sort | tr -d '\r' | uniq -c | sort -u | sort -zn | tail -n 6
return 0