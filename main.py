import nmap
import socket

def get_local_ip():
    """Local IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_network_range(ip):
    """Sub-network IP"""
    ip_parts = ip.split('.')
    ip_parts[-1] = '0/24'
    return '.'.join(ip_parts)

def scan_network_nmap(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sS -T4')  # you can change (-sS -T4) with other nmap atack types
    devices = []
    for host in nm.all_hosts():
        devices.append({
            "ip": host,
            "mac": nm[host]['addresses'].get('mac', 'N/A')
        })
    return devices

def print_devices(devices):
    print("Devices connected to the network:")
    for device in devices:
        print(f"IP: {device['ip']} \t MAC: {device['mac']}")

if __name__ == "__main__":
    local_ip = get_local_ip()
    network_range = get_network_range(local_ip)
    devices = scan_network_nmap(network_range)
    print_devices(devices)
