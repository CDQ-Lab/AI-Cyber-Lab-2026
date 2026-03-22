import subprocess
import xml.etree.ElementTree as ET
import requests
import sys
import argparse

# --- CONFIGURATION ---
# Default fallback values
DEFAULT_MODEL = "deepseek-r1:8b" 
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def run_nmap(target, ports=None):
    """Runs Nmap and returns raw XML. Supports subnets and specific ports."""
    print(f"[*] Executing network reconnaissance on: {target}")
    
    # -sV for version detection, -oX - to stream XML to stdout
    cmd = ['nmap', '-sV', '-oX', '-']
    if ports:
        cmd.extend(['-p', ports])
    cmd.append(target)
    
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return process.stdout
    except FileNotFoundError:
        print("[-] ERROR: Nmap is not installed or not in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error running nmap: {e}")
        return None

def parse_nmap_xml(xml_output):
    """Extracts IPs, ports, and services from the Nmap XML."""
    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError:
        print("[-] ERROR: Could not parse Nmap output.")
        return {}

    hosts_data = {}
    
    for host in root.findall('host'):
        # Extract the IPv4 address
        ip_element = host.find("address[@addrtype='ipv4']")
        if ip_element is None:
            continue
        ip_addr = ip_element.get('addr')
        
        services = []
        for port_element in host.findall('.//port'):
            port_id = port_element.get('portid')
            protocol = port_element.get('protocol')
            
            service_element = port_element.find('service')
            if service_element is not None:
                name = service_element.get('name', 'unknown')
                product = service_element.get('product', '')
                version = service_element.get('version', '')
            else:
                name, product, version = "unknown", "", ""

            services.append((port_id, protocol, name, product, version))
        
        if services:
            hosts_data[ip_addr] = services

    return hosts_data

def format_prompt(hosts_data, target_scope):
    """Builds the structured text message to send to the AI."""
    prompt = f"Network Scan Scope: {target_scope}\n\n"
    
    for ip, services in hosts_data.items():
        prompt += f"--- Target Host: {ip} ---\nServices found:\n"
        for s in services:
            prompt += f"Port {s[0]} ({s[1]}): {s[2]} {s[3]} {s[4]}\n"
        prompt += "\n"
        
    prompt += "Instructions:\n"
    prompt += "1. Analyze the risk level (Low/Medium/High) for the services on each host.\n"
    prompt += "2. For HIGH risk services, list specific exploit IDs (CVEs) or search terms for Exploit-DB.\n"
    prompt += "3. Keep the summary concise and professional, suitable for an intelligence brief."
    return prompt

def query_ollama(prompt, model, api_url):
    """Sends the prompt to the Ollama API (local or remote via VPN)."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        print(f"[*] Sending data to {model} via {api_url} for threat analysis...")
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        return response.json().get('response', 'No response field in JSON')
    except requests.exceptions.RequestException as e:
        print(f"[-] Error querying Ollama: {e}")
        return None

def main():
    # Setup command-line arguments (No more interactive inputs!)
    parser = argparse.ArgumentParser(description="AI-Powered Nmap Vulnerability Scanner v2.0")
    parser.add_argument("-t", "--target", required=True, help="Target IP or CIDR subnet (e.g., 127.0.0.1 or 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", help="Specific ports to scan (e.g., 80,443 or 1-1000)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("-u", "--url", default=OLLAMA_API_URL, help=f"Ollama API URL (default: {OLLAMA_API_URL})")
    
    args = parser.parse_args()

    # 1. Run Scan
    xml_output = run_nmap(args.target, args.ports)
    if not xml_output:
        return

    # 2. Parse Data
    hosts_data = parse_nmap_xml(xml_output)
    if not hosts_data:
        print("[-] No open ports found or scan failed.")
        return
        
    print(f"[+] Scan complete. Found {len(hosts_data)} live host(s) with open ports.")

    # 3. Ask AI
    prompt = format_prompt(hosts_data, args.target)
    analysis = query_ollama(prompt, args.model, args.url)
    
    # 4. Show Results
    if analysis:
        print("\n" + "="*55)
        print("EXECUTIVE THREAT INTELLIGENCE REPORT")
        print("="*55)
        print(analysis)

if __name__ == "__main__":
    main()