import pyshark

# Fungsi untuk memeriksa paket mencurigakan
def search_suspicious_packets(pcap_file):
    suspicious_packets = []
    
    # Membuka file pcap dengan filter dasar
    capture = pyshark.FileCapture(pcap_file, keep_packets=False)

    for packet in capture:
        # Mencari paket HTTP
        if 'http' in packet:
            if hasattr(packet.http, 'request_uri'):
                # Cek jika ada parameter query yang mencurigakan dalam HTTP request
                if 'password' in packet.http.request_uri.lower():
                    suspicious_packets.append(f"Suspicious HTTP Request: {packet.http.request_uri}")
                elif 'file' in packet.http.request_uri.lower():
                    suspicious_packets.append(f"Suspicious HTTP Request: {packet.http.request_uri}")
                
            if hasattr(packet.http, 'user_agent'):
                user_agent = packet.http.user_agent.lower()
                if "curl" in user_agent or "wget" in user_agent:
                    suspicious_packets.append(f"Suspicious User-Agent: {packet.http.user_agent}")

        # Mencari DNS query yang mencurigakan
        if 'dns' in packet:
            if hasattr(packet.dns, 'qry_name'):
                dns_query = packet.dns.qry_name.lower()
                if "file" in dns_query or "ftp" in dns_query:
                    suspicious_packets.append(f"Suspicious DNS Query: {packet.dns.qry_name}")
        
        # Mencari payload besar dalam TCP
        if 'tcp' in packet:
            if hasattr(packet.tcp, 'payload') and len(packet.tcp.payload) > 100:
                suspicious_packets.append(f"Large TCP Payload: {len(packet.tcp.payload)} bytes")

    return suspicious_packets

# Path ke file pcap yang ingin dipindai
pcap_file = 'challenge.pcapng'

# Menjalankan fungsi pemindaian
suspicious_packets = search_suspicious_packets(pcap_file)

# Menampilkan hasil
if suspicious_packets:
    print("Suspicious packets found:")
    for packet in suspicious_packets:
        print(packet)
else:
    print("No suspicious packets found.")

