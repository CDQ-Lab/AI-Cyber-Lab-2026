import subprocess
import xml.etree.ElementTree as ET
import requests
import sys

# --- CONFIGURATION ---
# Set default to the model you have installed.
DEFAULT_MODEL = "deepseek-r1:8b" 
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def run_nmap(target_ip):
    """Runs the Nmap scan and returns the raw XML output."""
    print(f"[*] Starting Nmap scan on {target_ip}...")
    # -oX - tells nmap to output XML to the screen so Python can grab it
    cmd = ['nmap', '-sV', '-oX', '-', target_ip]
    
    try:
        # We use standard subprocess call that works on Windows/Linux
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return process.stdout
    except FileNotFoundError:
        print("ERROR: Nmap is not installed or not in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")
        return None

def parse_nmap_xml(xml_output):
    """Extracts port and service info from the Nmap XML."""
    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError:
        print("ERROR: Could not parse Nmap output. Did the scan finish?")
        return []

    services = []
    # Correct logic: Find 'host', then 'ports', then 'port'
    for host in root.findall('host'):
        for port_element in host.findall('.//port'):
            # The Port ID is an attribute of the <port> tag
            port_id = port_element.get('portid')
            protocol = port_element.get('protocol')
            
            # The Service details are inside the child <service> tag
            service_element = port_element.find('service')
            if service_element is not None:
                name = service_element.get('name', 'unknown')
                product = service_element.get('product', '')
                version = service_element.get('version', '')
            else:
                name = "unknown"
                product = ""
                version = ""

            services.append((port_id, protocol, name, product, version))
    return services

def format_prompt(services, target_ip):
    """Builds the text message to send to the AI."""
    prompt = f"Target IP: {target_ip}\nServices found:\n"
    for s in services:
        # s[0]=port, s[1]=proto, s[2]=name, s[3]=product, s[4]=version
        prompt += f"Port {s[0]} ({s[1]}): {s[2]} {s[3]} {s[4]}\n"
        
    prompt += "\nInstructions:\n"
    prompt += "1. Analyze the risk level (Low/Medium/High) for each service.\n"
    prompt += "2. For HIGH risk services, list specific exploit IDs (CVEs) or search terms for Exploit-DB.\n"
    prompt += "3. Keep the summary concise."
    return prompt

def query_ollama(prompt, model=DEFAULT_MODEL):
    """Sends the prompt to your local AI and gets the answer."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        print(f"[*] Sending analysis request to {model}...")
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json().get('response', 'No response field in JSON')
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return None

def main():
    # 1. Get Target
    target_ip = input("Enter target IP (e.g., 127.0.0.1): ")
    
    # 2. Run Scan
    xml_output = run_nmap(target_ip)
    if not xml_output:
        return

    # 3. Parse Data
    services = parse_nmap_xml(xml_output)
    if not services:
        print("No open ports found or scan failed.")
        return
        
    print(f"[*] Found {len(services)} open ports/services.")

    # 4. Ask AI
    prompt = format_prompt(services, target_ip)
    analysis = query_ollama(prompt)
    
    # 5. Show Results
    if analysis:
        print("\n" + "="*40)
        print("AI SECURITY REPORT")
        print("="*40)
        print(analysis)

if __name__ == "__main__":

    main()
