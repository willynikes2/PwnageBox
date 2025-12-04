#!/usr/bin/env python3
"""
============================================================================
Cisco Router Traffic Simulator
============================================================================
Generates realistic-looking Cisco IOS syslog messages and sends them to
Splunk HEC. This creates background "noise" to make the dashboard appear
more realistic and live.
============================================================================
"""

import os
import sys
import time
import json
import random
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =============================================================================
# Configuration
# =============================================================================
SPLUNK_HEC_URL = os.getenv('SPLUNK_HEC_URL', 'https://splunk:8088/services/collector/event')
SPLUNK_HEC_TOKEN = os.getenv('SPLUNK_HEC_TOKEN', 'pwnagebox-hec-token-2024')
INTERVAL_SECONDS = 2

# =============================================================================
# Simulated Network Data
# =============================================================================

# Geographic locations for threat map
LOCATIONS = [
    {'city': 'Beijing', 'country': 'CN', 'lat': 39.9042, 'lon': 116.4074},
    {'city': 'Moscow', 'country': 'RU', 'lat': 55.7558, 'lon': 37.6173},
    {'city': 'São Paulo', 'country': 'BR', 'lat': -23.5505, 'lon': -46.6333},
    {'city': 'Mumbai', 'country': 'IN', 'lat': 19.0760, 'lon': 72.8777},
    {'city': 'Lagos', 'country': 'NG', 'lat': 6.5244, 'lon': 3.3792},
    {'city': 'Tehran', 'country': 'IR', 'lat': 35.6892, 'lon': 51.3890},
    {'city': 'Pyongyang', 'country': 'KP', 'lat': 39.0392, 'lon': 125.7625},
    {'city': 'Caracas', 'country': 'VE', 'lat': 10.4806, 'lon': -66.9036},
    {'city': 'Shanghai', 'country': 'CN', 'lat': 31.2304, 'lon': 121.4737},
    {'city': 'St Petersburg', 'country': 'RU', 'lat': 59.9311, 'lon': 30.3609},
    {'city': 'Hanoi', 'country': 'VN', 'lat': 21.0285, 'lon': 105.8542},
    {'city': 'Cairo', 'country': 'EG', 'lat': 30.0444, 'lon': 31.2357},
    {'city': 'Jakarta', 'country': 'ID', 'lat': -6.2088, 'lon': 106.8456},
    {'city': 'Berlin', 'country': 'DE', 'lat': 52.5200, 'lon': 13.4050},
    {'city': 'London', 'country': 'GB', 'lat': 51.5074, 'lon': -0.1278},
]

# Cisco router hostnames
ROUTERS = [
    'CORE-RTR-01', 'CORE-RTR-02', 'EDGE-FW-01', 'EDGE-FW-02',
    'DMZ-RTR-01', 'WAN-RTR-01', 'DIST-SW-01', 'DIST-SW-02'
]

# Cisco syslog facilities and severities
FACILITIES = ['SEC', 'SYS', 'IF', 'OSPF', 'BGP', 'ACL', 'NAT', 'VPN']
SEVERITIES = ['ALERT', 'CRIT', 'ERR', 'WARNING', 'NOTICE', 'INFO']

# ACL action types
ACL_ACTIONS = ['permit', 'deny']

# Common ports for traffic
PORTS = [22, 23, 25, 53, 80, 443, 445, 1433, 3306, 3389, 8080, 8443]

# Protocols
PROTOCOLS = ['TCP', 'UDP', 'ICMP']


def generate_ip():
    """Generate a random public IP address."""
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def generate_cisco_syslog():
    """Generate a realistic Cisco IOS syslog message."""
    router = random.choice(ROUTERS)
    facility = random.choice(FACILITIES)
    severity = random.choice(SEVERITIES)
    
    # Weight towards more INFO/WARNING messages
    if random.random() > 0.3:
        severity = random.choice(['INFO', 'NOTICE', 'WARNING'])
    
    messages = []
    
    if facility == 'ACL':
        action = random.choice(ACL_ACTIONS)
        src_ip = generate_ip()
        dst_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        protocol = random.choice(PROTOCOLS)
        src_port = random.randint(1024, 65535)
        dst_port = random.choice(PORTS)
        
        location = random.choice(LOCATIONS)
        
        return {
            'type': 'firewall',
            'router': router,
            'facility': facility,
            'severity': severity,
            'action': action,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'src_country': location['country'],
            'src_city': location['city'],
            'src_lat': location['lat'],
            'src_lon': location['lon'],
            'message': f"%{facility}-{random.randint(1,7)}-{action.upper()}: {action} {protocol.lower()} src={src_ip}:{src_port} dst={dst_ip}:{dst_port}"
        }
    
    elif facility == 'SEC':
        event_types = [
            'LOGIN_SUCCESS', 'LOGIN_FAILED', 'LOGOUT', 
            'SSH_SESSION', 'PRIV_EXEC_MODE', 'CONFIG_CHANGE'
        ]
        event = random.choice(event_types)
        user = random.choice(['admin', 'netops', 'readonly', 'backup'])
        src_ip = generate_ip()
        location = random.choice(LOCATIONS)
        
        return {
            'type': 'security',
            'router': router,
            'facility': facility,
            'severity': severity,
            'event': event,
            'user': user,
            'src_ip': src_ip,
            'src_country': location['country'],
            'src_city': location['city'],
            'src_lat': location['lat'],
            'src_lon': location['lon'],
            'message': f"%{facility}-{random.randint(1,7)}-{event}: User '{user}' from {src_ip}"
        }
    
    elif facility == 'IF':
        interface = f"GigabitEthernet0/{random.randint(0,48)}"
        states = ['UP', 'DOWN', 'ADMIN_DOWN', 'ERR_DISABLED']
        state = random.choice(states)
        
        return {
            'type': 'interface',
            'router': router,
            'facility': facility,
            'severity': severity,
            'interface': interface,
            'state': state,
            'message': f"%{facility}-{random.randint(1,7)}-UPDOWN: Interface {interface} changed state to {state}"
        }
    
    else:
        # Generic syslog
        return {
            'type': 'system',
            'router': router,
            'facility': facility,
            'severity': severity,
            'message': f"%{facility}-{random.randint(1,7)}-GENERAL: System event on {router}"
        }


def send_to_splunk(session, event_data):
    """Send event to Splunk HEC."""
    payload = {
        'event': {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'sourcetype': 'cisco:ios',
            'source': 'traffic_generator',
            **event_data
        }
    }
    
    try:
        response = session.post(
            SPLUNK_HEC_URL,
            json=payload,
            verify=False,
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"[!] Error sending to Splunk: {e}")
        return False


def wait_for_splunk(session, max_retries=30):
    """Wait for Splunk HEC to become available."""
    print("[*] Waiting for Splunk HEC to become available...")
    
    for attempt in range(max_retries):
        try:
            response = session.post(
                SPLUNK_HEC_URL,
                json={'event': {'message': 'Traffic generator startup'}},
                verify=False,
                timeout=5
            )
            if response.status_code in [200, 400]:
                print(f"[+] Splunk HEC connected after {attempt + 1} attempts")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"[*] Attempt {attempt + 1}/{max_retries}...")
        time.sleep(5)
    
    return False


def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║            Cisco Router Traffic Simulator                      ║
    ║               Background Noise Generator                       ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Setup session
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Splunk {SPLUNK_HEC_TOKEN}',
        'Content-Type': 'application/json'
    })
    
    # Wait for Splunk
    if not wait_for_splunk(session):
        print("[!] Warning: Could not connect to Splunk, continuing anyway...")
    
    print(f"[*] Starting traffic generation (interval: {INTERVAL_SECONDS}s)")
    
    event_count = 0
    
    while True:
        try:
            # Generate 1-3 events per cycle
            for _ in range(random.randint(1, 3)):
                event = generate_cisco_syslog()
                
                if send_to_splunk(session, event):
                    event_count += 1
                    action_str = event.get('action', event.get('event', 'LOG'))
                    src_str = event.get('src_ip', event.get('router', 'N/A'))
                    print(f"[{event_count}] {event['type'].upper()}: {action_str} from {src_str}")
            
            time.sleep(INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            print(f"\n[*] Stopping traffic generator. Total events: {event_count}")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
