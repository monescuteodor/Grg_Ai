Advanced Cyber-Physical Systems & Industrial IoT Complete Reference
CHAPTER 1: GETTING STARTED WITH CYBER-PHYSICAL SYSTEMS
Remarks
Cyber-Physical Systems (CPS) integrate computation, networking, and physical processes. Embedded computers and networks monitor and control the physical processes, usually with feedback loops where physical processes affect computations and vice versa. Key areas: SCADA (Supervisory Control and Data Acquisition), PLC (Programmable Logic Controllers), Industrial IoT (IIoT), Real-Time Operating Systems (RTOS) for industry, and Safety-Critical Systems. Applications: Smart grids, autonomous manufacturing, water treatment plants, medical devices, transportation systems.
Tools: Python (PyModbus, Scapy), Wireshark, OpenPLC, Node-RED, MQTT brokers (Mosquitto), Siemens TIA Portal (simulation).
Hello CPS
# hello_cps.py
"""
First CPS program: Simulate a simple temperature sensor and controller loop.
"""
import time
import random

class TemperatureSensor:
    def __init__(self, initial_temp=20.0):
        self.temp = initial_temp
        
    def read(self):
        # Simulate noise
        return self.temp + random.uniform(-0.5, 0.5)
        
    def update(self, heater_on):
        if heater_on:
            self.temp += 0.2
        else:
            self.temp -= 0.1
        # Ambient cooling/heating drift
        self.temp += random.uniform(-0.05, 0.05)

class PIDController:
    def __init__(self, Kp=1.0, Ki=0.1, Kd=0.05, setpoint=25.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0
        
    def compute(self, measurement):
        error = self.setpoint - measurement
        self.integral += error
        derivative = error - self.prev_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        # Output is boolean for heater on/off
        return output > 0

# Simulation
sensor = TemperatureSensor(20.0)
controller = PIDController(setpoint=25.0)

print("=== CPS Simulation Loop ===")
for i in range(20):
    temp = sensor.read()
    heater_on = controller.compute(temp)
    sensor.update(heater_on)
    status = "ON" if heater_on else "OFF"
    print(f"Step {i+1}: Temp={temp:.2f}°C, Heater={status}")

SCADA Architecture
# 1. Field Level: Sensors, actuators, PLCs.
# 2. Control Level: PLCs, RTUs (Remote Terminal Units).
# 3. Supervisory Level: HMI (Human-Machine Interface), SCADA server.
# 4. Enterprise Level: ERP, MES (Manufacturing Execution Systems).

Protocols
# Modbus TCP/RTU: Simple, master-slave, widely used.
# OPC UA: Secure, object-oriented, interoperable.
# MQTT: Lightweight publish-subscribe for IIoT.
# DNP3: Used in electric utilities.
# Profinet/EtherNet/IP: Industrial Ethernet standards.

CHAPTER 2: INDUSTRIAL PROTOCOLS
Modbus TCP Simulation
# Modbus uses Function Codes to read/write registers.
# FC 03: Read Holding Registers
# FC 06: Write Single Register
# FC 16: Write Multiple Registers

import socket
import struct

def modbus_read_holding_registers(ip, port, slave_id, start_addr, count):
    """Simulate a Modbus TCP read request."""
    # Transaction ID, Protocol ID, Length, Unit ID, Function Code, Start Addr, Count
    header = struct.pack('>HHHB', 0x0001, 0x0000, 0x0006, slave_id)
    payload = struct.pack('>BHH', 0x03, start_addr, count)
    
    # In a real scenario, send via socket
    # sock.send(header + payload)
    # response = sock.recv(1024)
    
    # Simulated response
    print(f"Requesting registers {start_addr} to {start_addr+count-1} from slave {slave_id}")
    return [random.randint(0, 65535) for _ in range(count)]

# Example
regs = modbus_read_holding_registers("192.168.1.10", 502, 1, 0, 5)
print(f"Register Values: {regs}")

MQTT for IIoT
# Publish/Subscribe model.
# Broker mediates communication.
# Topics: factory/machine1/temp, factory/machine1/status

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("factory/sensor/#")

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("localhost", 1883, 60)
# client.loop_start()
# client.publish("factory/sensor/temp", "25.5")
# client.loop_stop()

OPC UA Basics
# Address Space: Nodes, Objects, Variables.
# Services: Read, Write, Subscribe, Call.
# Security: Signatures, Encryption, Certificates.

CHAPTER 3: REAL-TIME CONSTRAINTS
Hard vs Soft Real-Time
# Hard Real-Time: Missing deadline causes system failure (e.g., airbag deployment).
# Soft Real-Time: Degraded performance if deadline missed (e.g., video streaming).

Scheduling Algorithms
# Rate Monotonic (RM): Fixed priority, shorter period = higher priority.
# Earliest Deadline First (EDF): Dynamic priority, earliest deadline = highest priority.

def rate_monotonic_schedule(tasks):
    """
    Tasks: list of (period, execution_time, name)
    Returns: Schedule order based on RM.
    """
    # Sort by period (ascending)
    sorted_tasks = sorted(tasks, key=lambda x: x[0])
    return [t[2] for t in sorted_tasks]

tasks = [
    (10, 2, "Control Loop"),
    (50, 5, "Data Logging"),
    (20, 3, "Safety Check")
]

order = rate_monotonic_schedule(tasks)
print(f"RM Schedule Order: {order}")

Jitter and Latency
# Jitter: Variation in latency.
# Latency: Time from event to response.
# Critical in control loops to maintain stability.

CHAPTER 4: SAFETY AND SECURITY IN CPS
Safety Standards
# IEC 61508: Functional safety of electrical/electronic/programmable electronic safety-related systems.
# ISO 26262: Road vehicles functional safety.
# SIL (Safety Integrity Level): SIL 1 to SIL 4.

Security Threats
# Replay Attacks: Capturing and re-sending valid commands.
# Man-in-the-Middle: Intercepting and modifying traffic.
# Denial of Service: Overloading PLCs or networks.
# Firmware Tampering: Modifying PLC logic.

Secure Communication
# TLS/SSL for MQTT (MQTTS).
# OPC UA Security Policies.
# VPNs for remote access.
# Network Segmentation (DMZ for industrial networks).

Intrusion Detection for ICS
# Anomaly detection in Modbus/OPC UA traffic.
# Whitelisting allowed commands.
# Monitoring for unusual register writes.

CHAPTER 5: DIGITAL TWINS
Concept
# Virtual replica of a physical system.
# Synchronized via real-time data.
# Used for simulation, prediction, and optimization.

Implementation
# 1. Physical Model: Physics-based equations (FEM, CFD).
# 2. Data Model: Sensor data integration.
# 3. Connection: Bidirectional data flow.

Benefits
# Predictive Maintenance: Detect wear before failure.
# Process Optimization: Test changes in virtual environment.
# Remote Monitoring: Visualize state from anywhere.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Edge Computing in CPS
# Processing data close to the source.
# Reduces latency and bandwidth usage.
# Platforms: AWS IoT Greengrass, Azure IoT Edge.

5G for Industrial Automation
# Ultra-Reliable Low-Latency Communication (URLLC).
# Enables wireless control loops.
# Network Slicing for dedicated industrial traffic.

Formal Verification of PLC Code
# Using model checking to verify ladder logic.
# Ensures safety properties hold under all conditions.

Recommended Reading
# - "Cyber-Physical Systems: A Perspective at the Centennial" by Lee
# - "Industrial Network Security" by Eric D. Knapp
# - "Real-Time Systems" by Jane W. S. Liu
# - OPC Foundation Documentation: https://opcfoundation.org/
# - Modbus Organization: https://modbus.org/

# End of Cyber-Physical Systems Reference