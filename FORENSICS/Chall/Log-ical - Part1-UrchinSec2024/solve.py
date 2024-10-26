import re
from collections import Counter

# Replace with the path to your access.log file
log_file = 'access.log'

# Define a set to store attacker IPs and a Counter to count requests
attacker_ips = set()
request_counts = Counter()

# Read the log file and process each line
with open(log_file, 'r') as f:
    for line in f:
        # Extract the IP address and request details
        ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+)', line)
        if ip_match:
            ip = ip_match.group(1)
            request_counts[ip] += 1
            
            # Identify suspicious activity (customize this condition)
            if "sql" in line.lower() or "union" in line.lower() or "drop" in line.lower():
                attacker_ips.add(ip)

# Identify the most frequent IP, assuming it's the victim's IP
victim_ip = request_counts.most_common(1)[0][0] if request_counts else 'unknown_victim'
# Assuming the first entry in attacker_ips is the attacker
attacker_ip = next(iter(attacker_ips), 'unknown_attacker')

# Format the result
result = f'urchinsec{{{attacker_ip}_{victim_ip}}}'
print(result)

