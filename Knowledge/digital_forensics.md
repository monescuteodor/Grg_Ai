Digital Forensics & Incident Response Complete Reference
CHAPTER 1: GETTING STARTED WITH DIGITAL FORENSICS
Remarks
Digital Forensics is the application of investigation and analysis techniques to gather and preserve evidence from a particular computing device in a way that is suitable for presentation in a court of law. Incident Response (IR) is the process of handling a cyberattack or data breach. Key phases: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned. Tools: Autopsy, Volatility, Wireshark, FTK Imager, dd, hexedit, strings, grep.
Tools: Python (for scripting), Autopsy (GUI), Volatility 3 (memory forensics), Wireshark (network), Sleuth Kit (file systems).
Hello Forensics
# hello_forensics.py
"""
First forensics program: Calculate hash of a file to verify integrity.
"""
import hashlib
import os

def calculate_hash(file_path, algorithm='sha256'):
    """Calculate hash of a file."""
    h = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# Example
test_file = "test.txt"
with open(test_file, 'w') as f:
    f.write("Evidence content")

hash_val = calculate_hash(test_file)
print(f"SHA-256 Hash: {hash_val}")
os.remove(test_file)

Forensic Soundness
# 1. Acquire: Create a bit-for-bit copy (image) of the media.
# 2. Authenticate: Verify the copy matches the original (Hashing).
# 3. Analyze: Examine the copy, never the original.
# 4. Document: Keep a strict chain of custody.

# Write Blockers: Hardware devices that prevent writing to the source drive.

CHAPTER 2: DISK FORENSICS
File Systems Analysis
# NTFS (Windows): MFT (Master File Table), $LogFile, $UsnJrnl.
# EXT4 (Linux): Inodes, Journal.
# FAT32/exFAT: File Allocation Table.

# Deleted files are often just marked as unallocated space. Data remains until overwritten.

import struct

def parse_ntfs_mft_entry(entry_data):
    """Simplified MFT entry parser."""
    # Signature "FILE"
    if entry_data[:4] != b'FILE':
        return None
    
    # Update Sequence Array offset
    usa_offset = struct.unpack_from('<H', entry_data, 4)[0]
    
    # Attributes start at this offset
    attr_offset = struct.unpack_from('<I', entry_data, 20)[0]
    
    return {"usa_offset": usa_offset, "attr_offset": attr_offset}

# Example: Read first 1024 bytes of an MFT entry (simplified)
# In real forensics, use The Sleuth Kit (tsk_recover)

Carving Files
# File Carving: Recovering files based on headers/footers, ignoring file system metadata.
# Magic Bytes:
# JPEG: FF D8 FF
# PNG: 89 50 4E 47
# PDF: 25 50 44 46
# ZIP: 50 4B 03 04

def carve_jpegs(image_path, output_dir):
    """Carve JPEGs from a raw disk image."""
    with open(image_path, 'rb') as f:
        data = f.read()
    
    start_marker = b'\xFF\xD8\xFF'
    end_marker = b'\xFF\xD9'
    
    start_idx = 0
    count = 0
    
    while True:
        start = data.find(start_marker, start_idx)
        if start == -1:
            break
        
        end = data.find(end_marker, start)
        if end == -1:
            break
        
        jpeg_data = data[start:end+2]
        out_path = os.path.join(output_dir, f"carved_{count}.jpg")
        with open(out_path, 'wb') as out:
            out.write(jpeg_data)
        
        count += 1
        start_idx = end + 2
        
    print(f"Carved {count} JPEGs.")

# Example usage (requires a raw .img file)
# carve_jpegs("disk.img", "output")

Timeline Analysis
# Super Timeline: Combining timestamps from MFT, Registry, Event Logs, Browser History.
# Tools: Plaso (log2timeline), Timesketch.

CHAPTER 3: MEMORY FORENSICS
Volatility Framework
# Volatility analyzes RAM dumps (.raw, .dmp, .vmem).
# Plugins: pslist, netscan, cmdscan, dumpfiles.

import subprocess

def run_volatility_plugin(image_path, plugin, profile="Win10x64"):
    """Run a Volatility 3 plugin."""
    cmd = [
        "vol", 
        "-f", image_path, 
        plugin
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Example: List processes
# print(run_volatility_plugin("memory.dmp", "windows.pslist"))

Process Hollowing Detection
# Process Hollowing: A technique where malware replaces the code of a legitimate process.
# Signs:
# 1. Mismatch between PEB (Process Environment Block) path and loaded modules.
# 2. Unusual memory permissions (RWX).
# 3. Disconnected VADs (Virtual Address Descriptors).

def check_process_integrity(pid):
    """Check for signs of process hollowing (conceptual)."""
    # In real implementation, use Volatility or Windows API
    # 1. Get PEB path
    # 2. Get loaded DLLs
    # 3. Compare paths
    pass

CHAPTER 4: NETWORK FORENSICS
PCAP Analysis
# PCAP (Packet Capture) files contain network traffic.
# Tools: Wireshark, tshark, tcpdump.

import pyshark

def analyze_pcap(pcap_file):
    """Analyze a PCAP file for HTTP requests."""
    cap = pyshark.FileCapture(pcap_file)
    http_requests = []
    
    for packet in cap:
        if hasattr(packet, 'http'):
            if hasattr(packet.http, 'request_uri'):
                http_requests.append({
                    'src': packet.ip.src,
                    'dst': packet.ip.dst,
                    'uri': packet.http.request_uri
                })
    
    cap.close()
    return http_requests

# Example
# reqs = analyze_pcap("traffic.pcap")
# for r in reqs:
#     print(f"{r['src']} -> {r['dst']}: {r['uri']}")

DNS Tunneling Detection
# DNS Tunneling: Encoding data in DNS queries to bypass firewalls.
# Signs:
# 1. High volume of TXT or CNAME records.
# 2. Long, random-looking subdomains.
# 3. High entropy in domain names.

def detect_dns_tunneling(dns_logs):
    """Detect potential DNS tunneling."""
    suspicious = []
    for log in dns_logs:
        domain = log['query']
        # Check entropy
        entropy = calculate_entropy(domain.split('.')[0])
        if entropy > 3.5 and len(domain) > 50:
            suspicious.append(log)
    return suspicious

def calculate_entropy(s):
    """Calculate Shannon entropy."""
    import math
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return -sum([p * math.log2(p) for p in prob if p > 0])

CHAPTER 5: INCIDENT RESPONSE LIFECYCLE
Preparation
# 1. Policy Development: Define what constitutes an incident.
# 2. Team Creation: CSIRT (Computer Security Incident Response Team).
# 3. Tooling: SIEM, EDR, Forensic kits.
# 4. Communication Plan: Who to notify?

Identification
# 1. Alert Triage: Is it a false positive?
# 2. Scope Determination: How many systems are affected?
# 3. Evidence Preservation: Image disks, capture memory.

Containment
# Short-term: Isolate infected hosts (VLAN change, firewall block).
# Long-term: Apply patches, update signatures.

Eradication
# Remove malware, delete attacker accounts, close backdoors.

Recovery
# Restore from clean backups.
# Monitor for re-infection.

Lessons Learned
# Post-Incident Report.
# Update policies and tools.

CHAPTER 6: MALWARE ANALYSIS BASICS
Static Analysis
# 1. Hashing: Identify known malware.
# 2. Strings: Extract readable text.
# 3. PE Header Analysis: Check imports, sections, timestamps.

import pefile

def analyze_pe(pe_path):
    """Basic static analysis of a PE file."""
    pe = pefile.PE(pe_path)
    
    # Imports
    imports = []
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                imports.append(imp.name.decode())
    
    # Sections
    sections = []
    for section in pe.sections:
        sections.append({
            'name': section.Name.decode().rstrip('\x00'),
            'entropy': section.get_entropy(),
            'size': section.SizeOfRawData
        })
        
    return {"imports": imports[:10], "sections": sections}

# Example
# print(analyze_pe("malware.exe"))

Dynamic Analysis
# 1. Sandbox: Run malware in isolated VM.
# 2. Monitoring: Process Monitor, Wireshark, RegShot.
# 3. Behavior: File creation, registry changes, network connections.

Anti-Analysis Techniques
# 1. Packing: Compress/encrypt code to hide signature.
# 2. Obfuscation: Rename variables, insert junk code.
# 3. Anti-VM: Check for virtualization artifacts.
# 4. Debugging Detection: Check for debuggers attached.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Steganography
# Hiding data within other files (images, audio).
# Tools: Steghide, OpenStego.

Mobile Forensics
# Android: ADB backups, SQLite databases.
# iOS: iTunes backups, keychain extraction.

Cloud Forensics
# Challenges: Multi-tenancy, lack of physical access.
# Sources: CloudTrail logs, S3 bucket logs, VM snapshots.

Recommended Reading
# - "Digital Forensics and Incident Response" by Gerard Johansen
# - "Practical Malware Analysis" by Sikorski and Honig
# - "The Art of Memory Forensics" by Ligh et al.
# - SANS Institute Forensics Courses

# Online Resources
# - Volatility Foundation: https://www.volatilityfoundation.org/
# - Autopsy: https://www.autopsy.com/
# - Wireshark Wiki: https://wiki.wireshark.org/

# End of Digital Forensics & Incident Response Reference