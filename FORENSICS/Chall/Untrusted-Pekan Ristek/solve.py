from scapy.all import *
import re

# Load the .pcapng file
pcap = rdpcap('challenc.pcapng')

# Set up patterns to match common ransomware behavior in network traffic
patterns = [
    r"nc.*-e.*sh",
    r"wget.*http",
    r"curl.*http",
]

# Iterate through packets and search for matching patterns
for packet in pcap:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        raw_data = packet[Raw].load.decode(errors='ignore')
        for pattern in patterns:
            if re.search(pattern, raw_data):
                print(f"Suspicious command found: {raw_data}")

