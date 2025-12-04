#!/usr/bin/env python3
"""
============================================================================
PwnageBox Auto-Pwn Engine
============================================================================
Simulates a complete attack chain:
  1. RECON    - Nmap scan of target
  2. VULN     - CVE identification from service banners
  3. EXPLOIT  - Simulated Metasploit module execution
  4. SUCCESS  - Root shell establishment

All stages are logged to Splunk HEC for dashboard visualization.
============================================================================
"""

import os
import sys
import time
import json
import socket
import subprocess
import requests
from datetime import datetime
from typing import Optional, Dict, Any
import urllib3

# Disable SSL warnings for self-signed Splunk certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =============================================================================
# Configuration
# =============================================================================
SPLUNK_HEC_URL = os.getenv('SPLUNK_HEC_URL', 'https://splunk:8088/services/collector/event')
SPLUNK_HEC_TOKEN = os.getenv('SPLUNK_HEC_TOKEN', 'pwnagebox-hec-token-2024')
TARGET_HOST = os.getenv('TARGET_HOST', 'victim-ftp')
TARGET_PORT = int(os.getenv('TARGET_PORT', '21'))

# Attack chain stages
STAGES = ['INIT', 'RECON', 'VULN', 'EXPLOIT', 'SUCCESS', 'COMPLETE']

# Known vulnerability database (simulated)
VULN_DATABASE = {
    'vsftpd 2.3.4': {
        'cve': 'CVE-2011-2523',
        'description': 'vsftpd 2.3.4 Backdoor Command Execution',
        'severity': 'CRITICAL',
        'cvss': 10.0,
        'exploit_module': 'exploit/unix/ftp/vsftpd_234_backdoor',
        'backdoor_port': 6200
    },
    'ProFTPD 1.3.3c': {
        'cve': 'CVE-2010-4221',
        'description': 'ProFTPD 1.3.3c Telnet IAC Buffer Overflow',
        'severity': 'HIGH',
        'cvss': 7.5,
        'exploit_module': 'exploit/unix/ftp/proftpd_133c_backdoor'
    }
}


class SplunkLogger:
    """Handles logging to Splunk HEC with retry logic."""
    
    def __init__(self, hec_url: str, hec_token: str, max_retries: int = 10):
        self.hec_url = hec_url
        self.hec_token = hec_token
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Splunk {hec_token}',
            'Content-Type': 'application/json'
        })
        self._wait_for_splunk()
    
    def _wait_for_splunk(self):
        """Wait for Splunk HEC to become available."""
        print("[*] Waiting for Splunk HEC to become available...")
        for attempt in range(self.max_retries):
            try:
                # Test connection with a health check event
                response = self.session.post(
                    self.hec_url,
                    json={'event': {'message': 'PwnageBox connection test'}},
                    verify=False,
                    timeout=5
                )
                if response.status_code in [200, 400]:  # 400 means HEC is up but might reject test
                    print(f"[+] Splunk HEC connected after {attempt + 1} attempts")
                    return True
            except requests.exceptions.RequestException as e:
                print(f"[!] Attempt {attempt + 1}/{self.max_retries}: Splunk not ready - {e}")
            time.sleep(5)
        
        print("[!] Warning: Could not verify Splunk connection, proceeding anyway...")
        return False
    
    def log(self, stage: str, message: str, extra_fields: Optional[Dict[str, Any]] = None):
        """Send a log event to Splunk HEC."""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        event_data = {
            'event': {
                'timestamp': timestamp,
                'stage': stage,
                'message': message,
                'source': 'pwnagebox',
                'sourcetype': 'pwnagebox:attack',
                'host': socket.gethostname(),
                'target': TARGET_HOST
            }
        }
        
        if extra_fields:
            event_data['event'].update(extra_fields)
        
        # Also print to console for debugging
        color_codes = {
            'INIT': '\033[94m',      # Blue
            'RECON': '\033[96m',     # Cyan
            'VULN': '\033[93m',      # Yellow
            'EXPLOIT': '\033[91m',   # Red
            'SUCCESS': '\033[92m',   # Green
            'COMPLETE': '\033[95m'   # Magenta
        }
        reset = '\033[0m'
        color = color_codes.get(stage, '')
        print(f"{color}[{stage}]{reset} {message}")
        
        try:
            response = self.session.post(
                self.hec_url,
                json=event_data,
                verify=False,
                timeout=10
            )
            if response.status_code != 200:
                print(f"[!] Splunk HEC error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Failed to send log to Splunk: {e}")


class PwnageBox:
    """Main attack orchestration engine."""
    
    def __init__(self, logger: SplunkLogger):
        self.logger = logger
        self.target_host = TARGET_HOST
        self.target_port = TARGET_PORT
        self.discovered_services = {}
        self.vulnerabilities = []
    
    def run_attack_chain(self):
        """Execute the complete attack chain."""
        self.logger.log('INIT', f'PwnageBox initializing attack chain against {self.target_host}')
        time.sleep(2)
        
        # Stage 1: Reconnaissance
        self._stage_recon()
        time.sleep(3)
        
        # Stage 2: Vulnerability Analysis
        self._stage_vuln_analysis()
        time.sleep(2)
        
        # Stage 3: Exploitation
        self._stage_exploit()
        time.sleep(2)
        
        # Stage 4: Post-Exploitation
        self._stage_post_exploit()
        
        self.logger.log('COMPLETE', 'Attack chain completed successfully', {
            'total_vulns': len(self.vulnerabilities),
            'exploited': True
        })
    
    def _stage_recon(self):
        """Stage 1: Network reconnaissance using Nmap."""
        self.logger.log('RECON', f'Initiating port scan on {self.target_host}')
        time.sleep(1)
        
        # Try actual nmap scan first
        try:
            self.logger.log('RECON', f'Running: nmap -sV -p 21,22,23,80,443 {self.target_host}')
            
            result = subprocess.run(
                ['nmap', '-sV', '-p', '21,22,23,80,443', '--open', self.target_host],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            nmap_output = result.stdout
            self.logger.log('RECON', f'Nmap scan completed')
            
            # Parse nmap output for service detection
            if '21/tcp' in nmap_output and 'open' in nmap_output:
                self.logger.log('RECON', f'Port 21/tcp OPEN - FTP service detected', {
                    'port': 21,
                    'protocol': 'tcp',
                    'state': 'open',
                    'service': 'ftp'
                })
        except subprocess.TimeoutExpired:
            self.logger.log('RECON', 'Nmap scan timed out, using fallback method')
        except Exception as e:
            self.logger.log('RECON', f'Nmap error: {e}, using fallback method')
        
        # Fallback: Direct banner grab
        self._grab_banner()
    
    def _grab_banner(self):
        """Grab service banner directly via socket."""
        self.logger.log('RECON', f'Attempting banner grab on {self.target_host}:{self.target_port}')
        
        for attempt in range(5):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.target_host, self.target_port))
                
                # Receive banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                
                self.logger.log('RECON', f'Banner received: {banner}', {
                    'banner': banner,
                    'port': self.target_port
                })
                
                # Parse banner for version info
                if 'vsFTPd' in banner or 'vsftpd' in banner.lower():
                    version = self._extract_version(banner)
                    self.discovered_services['ftp'] = {
                        'port': self.target_port,
                        'banner': banner,
                        'software': 'vsftpd',
                        'version': version
                    }
                    self.logger.log('RECON', f'Service identified: vsftpd {version}', {
                        'software': 'vsftpd',
                        'version': version
                    })
                return
                
            except socket.timeout:
                self.logger.log('RECON', f'Connection timeout, attempt {attempt + 1}/5')
                time.sleep(2)
            except socket.error as e:
                self.logger.log('RECON', f'Connection error: {e}, attempt {attempt + 1}/5')
                time.sleep(2)
        
        # If we can't connect, simulate for demo purposes
        self.logger.log('RECON', 'Using simulated banner for demonstration')
        self.discovered_services['ftp'] = {
            'port': 21,
            'banner': '220 (vsFTPd 2.3.4)',
            'software': 'vsftpd',
            'version': '2.3.4'
        }
        self.logger.log('RECON', 'Port 21 Open - Banner: vsFTPd 2.3.4', {
            'software': 'vsftpd',
            'version': '2.3.4'
        })
    
    def _extract_version(self, banner: str) -> str:
        """Extract version number from banner."""
        import re
        match = re.search(r'(\d+\.\d+\.?\d*)', banner)
        return match.group(1) if match else 'unknown'
    
    def _stage_vuln_analysis(self):
        """Stage 2: Vulnerability analysis and CVE matching."""
        self.logger.log('VULN', 'Analyzing discovered services for known vulnerabilities')
        
        for service_name, service_info in self.discovered_services.items():
            software = service_info.get('software', '')
            version = service_info.get('version', '')
            search_key = f"{software} {version}"
            
            self.logger.log('VULN', f'Searching vulnerability database for: {search_key}')
            time.sleep(1)
            
            # Check against our vulnerability database
            for vuln_key, vuln_data in VULN_DATABASE.items():
                if vuln_key.lower() in search_key.lower():
                    self.vulnerabilities.append({
                        'service': service_name,
                        'software': search_key,
                        **vuln_data
                    })
                    
                    self.logger.log('VULN', 
                        f'MATCH FOUND: {vuln_data["cve"]} ({vuln_data["description"]})', {
                            'cve': vuln_data['cve'],
                            'severity': vuln_data['severity'],
                            'cvss': vuln_data['cvss'],
                            'exploit_available': True
                        })
                    
                    self.logger.log('VULN', 
                        f'Severity: {vuln_data["severity"]} | CVSS: {vuln_data["cvss"]}', {
                            'cve': vuln_data['cve']
                        })
        
        if not self.vulnerabilities:
            self.logger.log('VULN', 'No known vulnerabilities found in database')
    
    def _stage_exploit(self):
        """Stage 3: Exploit execution."""
        if not self.vulnerabilities:
            self.logger.log('EXPLOIT', 'No exploitable vulnerabilities found')
            return
        
        for vuln in self.vulnerabilities:
            self.logger.log('EXPLOIT', 
                f'Preparing exploit for {vuln["cve"]}')
            time.sleep(1)
            
            self.logger.log('EXPLOIT', 
                f'Loading Metasploit module: {vuln["exploit_module"]}', {
                    'module': vuln['exploit_module'],
                    'cve': vuln['cve']
                })
            time.sleep(1)
            
            self.logger.log('EXPLOIT', 
                f'Setting RHOSTS => {self.target_host}')
            time.sleep(0.5)
            
            self.logger.log('EXPLOIT', 
                f'Setting RPORT => {self.target_port}')
            time.sleep(0.5)
            
            self.logger.log('EXPLOIT', 
                'Executing exploit...')
            time.sleep(2)
            
            # Simulate successful exploitation
            self.logger.log('EXPLOIT', 
                f'Exploit completed - Backdoor triggered on port 6200', {
                    'exploit_status': 'success',
                    'backdoor_port': 6200
                })
    
    def _stage_post_exploit(self):
        """Stage 4: Post-exploitation and shell establishment."""
        self.logger.log('SUCCESS', 
            'Connecting to backdoor shell...', {
                'stage': 'post_exploitation'
            })
        time.sleep(2)
        
        self.logger.log('SUCCESS', 
            '████████████████████████████████████████████████████████')
        self.logger.log('SUCCESS', 
            '██  ROOT SHELL ESTABLISHED - FULL SYSTEM COMPROMISE  ██', {
                'shell_type': 'root',
                'access_level': 'SYSTEM',
                'compromised': True
            })
        self.logger.log('SUCCESS', 
            '████████████████████████████████████████████████████████')
        
        time.sleep(1)
        
        # Simulate post-exploitation enumeration
        self.logger.log('SUCCESS', 'Enumerating compromised system...')
        time.sleep(1)
        
        system_info = {
            'hostname': 'victim-ftp',
            'os': 'Linux 5.4.0',
            'arch': 'x86_64',
            'user': 'root',
            'uid': 0
        }
        
        self.logger.log('SUCCESS', 
            f'System: {system_info["os"]} ({system_info["arch"]})', system_info)
        self.logger.log('SUCCESS', 
            f'User: {system_info["user"]} (UID: {system_info["uid"]})', system_info)
        
        time.sleep(1)
        self.logger.log('SUCCESS', 
            'Attack chain complete - Target fully compromised', {
                'attack_successful': True,
                'root_access': True
            })


def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗ ██╗    ██╗███╗   ██╗ █████╗  ██████╗ ███████╗      ║
    ║   ██╔══██╗██║    ██║████╗  ██║██╔══██╗██╔════╝ ██╔════╝      ║
    ║   ██████╔╝██║ █╗ ██║██╔██╗ ██║███████║██║  ███╗█████╗        ║
    ║   ██╔═══╝ ██║███╗██║██║╚██╗██║██╔══██║██║   ██║██╔══╝        ║
    ║   ██║     ╚███╔███╔╝██║ ╚████║██║  ██║╚██████╔╝███████╗      ║
    ║   ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ║
    ║                        BOX v2.0                               ║
    ║              AI-Powered Offensive Security                    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"[*] Target: {TARGET_HOST}:{TARGET_PORT}")
    print(f"[*] Splunk HEC: {SPLUNK_HEC_URL}")
    print()
    
    # Initialize Splunk logger
    logger = SplunkLogger(SPLUNK_HEC_URL, SPLUNK_HEC_TOKEN)
    
    # Initialize and run PwnageBox
    pwnbox = PwnageBox(logger)
    pwnbox.run_attack_chain()
    
    print("\n[*] PwnageBox attack simulation complete.")
    print("[*] Check Splunk dashboard for visualization.")
    
    # Keep container alive briefly for log flushing
    time.sleep(5)


if __name__ == '__main__':
    main()
