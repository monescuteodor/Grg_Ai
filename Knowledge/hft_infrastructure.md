High-Frequency Trading Infrastructure Complete Reference
CHAPTER 1: GETTING STARTED WITH HFT INFRASTRUCTURE
Remarks
High-Frequency Trading (HFT) relies on ultra-low latency systems to execute trades in microseconds or nanoseconds. Key challenges: minimizing network latency, reducing OS jitter, optimizing hardware utilization, and ensuring deterministic behavior. Technologies: FPGA, Kernel Bypass (DPDK, Solarflare), Lock-free Data Structures, CPU Pinning, NUMA Awareness.
Tools: C++, Rust, Python (for research), DPDK, Solarflare Onload, Wireshark, tcpdump, perf, chrony.
Hello Low Latency
# hello_latency.py
"""
First HFT program: Measure round-trip time of a simple socket connection.
"""
import socket
import time
import struct

def measure_rtt(host='127.0.0.1', port=9999, iterations=1000):
    """Measure Round-Trip Time (RTT) for TCP loopback."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    # Send a small payload
    payload = struct.pack('!d', time.time())
    
    times = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        client.send(payload)
        data = client.recv(8)
        end = time.perf_counter_ns()
        times.append(end - start)
        
    client.close()
    
    avg_rtt = sum(times) / len(times)
    min_rtt = min(times)
    max_rtt = max(times)
    
    print(f"Average RTT: {avg_rtt:.2f} ns")
    print(f"Min RTT:     {min_rtt:.2f} ns")
    print(f"Max RTT:     {max_rtt:.2f} ns")
    print(f"Jitter:      {max_rtt - min_rtt:.2f} ns")

# Note: Requires a simple echo server running on localhost
# measure_rtt()

Latency Budget
# Total Latency = Network Propagation + Serialization + Switching + OS Processing + Application Logic
# Typical Breakdown:
# - Fiber Optic: ~5 us/km
# - Switch: ~100-300 ns
# - NIC: ~1-5 us
# - OS Kernel: ~10-50 us (can be reduced to <1 us with bypass)
# - Application: <1 us (optimized C++/FPGA)

CHAPTER 2: KERNEL BYPASS & NETWORKING
DPDK (Data Plane Development Kit)
# Allows user-space applications to directly access NIC buffers.
# Avoids context switches and kernel overhead.
# Uses Poll Mode Drivers (PMD) instead of interrupts.

# Key Concepts:
# - Hugepages: Reduce TLB misses.
# - CPU Pinning: Dedicate cores to polling threads.
# - Memory Pools: Pre-allocate mbufs (packet buffers).

# Example: DPDK initialization (C pseudo-code)
"""
int main(int argc, char *argv[]) {
    rte_eal_init(argc, argv);
    struct rte_mempool *mbuf_pool = rte_pktmbuf_pool_create("MBUF_POOL", 
        NUM_MBUFS, MBUF_CACHE_SIZE, 0, RTE_MBUF_DEFAULT_BUF_SIZE, 
        rte_socket_id());
    // Initialize ports, queues, etc.
}
"""

Solarflare Onload
# User-level networking stack for Solarflare NICs.
# Intercepts socket calls and handles them in user space.
# Compatible with standard POSIX sockets.

# Usage:
# LD_PRELOAD=/usr/lib64/libonload.so ./my_trading_app

Lock-Free Ring Buffers
# Used for passing packets between NIC and application.
# Single Producer Single Consumer (SPSC) is fastest.

import ctypes
import multiprocessing

class SPSCRingBuffer:
    def __init__(self, size=1024):
        self.size = size
        self.buffer = multiprocessing.Array(ctypes.c_uint64, size)
        self.head = multiprocessing.Value('L', 0)
        self.tail = multiprocessing.Value('L', 0)
        
    def push(self, item):
        head = self.head.value
        next_head = (head + 1) % self.size
        if next_head == self.tail.value:
            return False  # Full
        self.buffer[head] = item
        self.head.value = next_head
        return True
        
    def pop(self):
        tail = self.tail.value
        if tail == self.head.value:
            return None  # Empty
        item = self.buffer[tail]
        self.tail.value = (tail + 1) % self.size
        return item

CHAPTER 3: HARDWARE ACCELERATION
FPGA (Field-Programmable Gate Array)
# Hardware logic for ultra-low latency processing.
# Used for: Packet parsing, order book matching, risk checks.
# Languages: Verilog, VHDL, SystemVerilog, HLS (High-Level Synthesis).

# Example: Simple Verilog module for timestamping
"""
module timestamp_adder (
    input wire clk,
    input wire [63:0] current_time,
    input wire [7:0] packet_data,
    output reg [71:0] tagged_packet
);
    always @(posedge clk) begin
        tagged_packet <= {current_time, packet_data};
    end
endmodule
"""

NIC Offloading
# Modern NICs can handle:
# - Checksum calculation
# - TCP segmentation offload (TSO)
# - Receive Side Scaling (RSS)
# - Timestamping (PTP - Precision Time Protocol)

Precision Time Protocol (PTP)
# IEEE 1588 standard for clock synchronization.
# Sub-microsecond accuracy across networked devices.
# Essential for correlating events across multiple servers.

CHAPTER 4: MEMORY OPTIMIZATION
NUMA Awareness
# Non-Uniform Memory Access.
# Accessing local memory is faster than remote memory.
# Strategy: Pin threads to cores and allocate memory on the same NUMA node.

# Linux commands:
# numactl --cpunodebind=0 --membind=0 ./trading_app

Cache Line Optimization
# False Sharing: Two threads modify variables on the same cache line.
# Solution: Padding to align data to 64-byte boundaries.

import struct

class CacheAlignedData:
    def __init__(self):
        self.value = 0
        self.padding = b'\x00' * 56  # Pad to 64 bytes

# Or use C++ alignas(64)

Hugepages
# Standard page size: 4 KB.
# Hugepage size: 2 MB or 1 GB.
# Benefits: Fewer TLB misses, less page table overhead.

# Linux configuration:
# echo 1024 > /proc/sys/vm/nr_hugepages

CHAPTER 5: OPERATING SYSTEM TUNING
CPU Isolation
# Reserve cores for critical threads.
# Prevent OS from scheduling other tasks on these cores.

# Linux kernel boot parameters:
# isolcpus=2-7 nohz_full=2-7 rcu_nocbs=2-7

Interrupt Affinity
# Bind NIC interrupts to specific cores.
# Prevent interrupt handling from interfering with trading logic.

# Command:
# echo 2 > /proc/irq/XX/smp_affinity_list

Real-Time Kernels
# PREEMPT_RT patch for Linux.
# Reduces maximum latency by making most kernel code preemptible.

CHAPTER 6: RISK MANAGEMENT & COMPLIANCE
Pre-Trade Risk Checks
# Must be performed in microseconds.
# Checks: Position limits, order size limits, price bands.
# Implementation: FPGA or optimized C++ on same host as strategy.

Order Book Reconstruction
# Maintain local copy of exchange order book.
# Use incremental updates (ITCH, OUCH protocols).
# Validate sequence numbers to detect drops.

Kill Switch
# Immediate cessation of trading activity.
# Hardware-level switch preferred for reliability.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Microwave Networks
# Lower latency than fiber for long distances.
# Used for cross-exchange arbitrage.

Co-location
# Placing servers in the same data center as exchange matching engines.
# Minimizes propagation delay.

Recommended Reading
# - "Ultra-Low Latency Market Data" by Michael A. Harris
# - "High-Frequency Trading" by Irene Aldridge
# - DPDK Documentation: https://doc.dpdk.org/
# - Solarflare Onload User Guide

# End of High-Frequency Trading Infrastructure Reference