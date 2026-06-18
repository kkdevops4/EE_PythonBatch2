import time
import random

# ==========================================
# 1. CUSTOM EXCEPTION HIERARCHY
# ==========================================
class OBDSensorError(Exception):
    """Base exception for all OBD-II diagnostic and sensor faults."""
    pass

class TimeoutError(OBDSensorError):
    """Raised when an ECU fails to respond within the designated time limit."""
    pass

class ChecksumError(OBDSensorError):
    """Raised when incoming data fails the integrity check due to corruption."""
    pass

class OfflineError(OBDSensorError):
    """Raised when the physical connection to the gateway network is severed."""
    pass


# ==========================================
# 2. FILE HANDLING: DATA LOG MANAGEMENT
# ==========================================
class DiagnosticLogger:
    def __init__(self, filename="obd_diagnostics.txt"):
        self.filename = filename
        with open(self.filename, "w") as file:
            file.write("=== OBD-II DIAGNOSTIC SYSTEM LOG START ===\n")

    def log_event(self, level, message):
        """Saves formal long logs to file, but prints short clean alerts to console."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Save the formal, detailed log to the text file
        file_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        with open(self.filename, "a") as file:
            file.write(file_entry)
            
        # 2. Print a simplified, user-friendly message to the Terminal Console
        if level.lower() == "success":
            print(f"  └─ ▶ SUCCESS: Data verified.")
        elif level.lower() == "warning":
            print(f"  └─ ⚠ WARNING: Transmission delayed (Timeout).")
        elif level.lower() == "error":
            print(f"  └─ ❌ ERROR: Packet corrupted (Checksum Mismatch).")
        elif level.lower() == "critical":
            print(f"  └─ ⛔ CRITICAL: Hardware Connection Lost!")
        else:
            print(f"\n{message}")


# ==========================================
# 3. ENVIRONMENT SETUP: CYCLIC BUS LOG GENERATOR
# ==========================================
def generate_raw_bus_data(filename="raw_sensor_data.txt", total_packets=12):
    """Generates raw sensor data in a strict cyclic sequence (Engine -> ABS -> Airbag)."""
    ecu_pool = ["Engine_ECU", "ABS_ECU", "Airbag_ECU"]
    
    with open(filename, "w") as file:
        for i in range(total_packets):
            # Deterministic round-robin index selection using modulo operator
            ecu_name = ecu_pool[i % len(ecu_pool)]
            
            if ecu_name == "Engine_ECU":
                val1 = random.randint(800, 4000)  # RPM
                val2 = random.randint(85, 105)    # Engine Temp
            elif ecu_name == "ABS_ECU":
                val1 = random.randint(0, 120)     # Speed kmh
                val2 = random.randint(30, 70)      # Brake PSI
            else:
                val1 = random.randint(1, 5)       # Airbag Status Code
                val2 = 101                        # Static Seed Value
                
            checksum = val1 ^ val2
            file.write(f"{ecu_name},{val1},{val2},{checksum}\n")
            
    print(f"-> Setup: Generated cyclic 'raw_sensor_data.txt' ({total_packets} sequential packets found).")


# ==========================================
# 4. GATEWAY ENGINE MANAGEMENT SYSTEM
# ==========================================
class OBDGateway:
    def __init__(self, logger):
        self.logger = logger
        self.is_cable_connected = True
        self.timeout_threshold = 1.0 

    def process_raw_line(self, raw_line):
        """Parses a raw line, checks transmission states, and validates integrity."""
        if not self.is_cable_connected:
            raise OfflineError("Hardware interface link down. Diagnostic bus isolated.")

        if random.randint(1, 15) == 7:
            self.is_cable_connected = False
            raise OfflineError("Fatal Error: Diagnostic wire link severed mid-transit.")

        cleaned_line = raw_line.strip()
        if not cleaned_line:
            return None 
            
        ecu_name, str_val1, str_val2, str_checksum = cleaned_line.split(",")
        val1 = int(str_val1)
        val2 = int(str_val2)
        received_checksum = int(str_checksum)

        simulated_latency = random.choice([random.uniform(0.1, 0.3), random.uniform(0.1, 0.3), random.uniform(1.1, 1.5)])
        if simulated_latency > self.timeout_threshold:
            raise TimeoutError(f"{ecu_name} transmission timed out. Latency: {simulated_latency:.2f}s")

        if random.randint(1, 10) == 5:
            val1 += 1 

        calculated_checksum = val1 ^ val2

        if calculated_checksum != received_checksum:
            raise ChecksumError(f"Data corruption detected on payload from {ecu_name}.")

        return {"Module": ecu_name, "Param1": val1, "Param2": val2}


# ==========================================
# 5. DIAGNOSTIC TOOL EXECUTION PIPELINE
# ==========================================
def run_system_scan():
    # Setting total packets to 12 means exactly 4 complete cycles of all 3 ECUs
    generate_raw_bus_data(filename="raw_sensor_data.txt", total_packets=12)
    
    logger = DiagnosticLogger(filename="obd_diagnostics.txt")
    gateway = OBDGateway(logger)
    
    logger.log_event("info", "=== Starting OBD-II Diagnostic Scanner ===")
    
    try:
        with open("raw_sensor_data.txt", "r") as input_file:
            packet_count = 0
            
            for line in input_file:
                if line.strip():
                    temp_ecu_name = line.split(",")[0]
                else:
                    continue
                    
                packet_count += 1
                logger.log_event("info", f"Reading Packet #{packet_count} [{temp_ecu_name}]...")
                time.sleep(0.3) 
                
                try:
                    parsed_data = gateway.process_raw_line(line)
                    if parsed_data:
                        logger.log_event("success", f"SUCCESS | {parsed_data['Module']} data parsed cleanly.")
                        
                except TimeoutError as err:
                    logger.log_event("warning", str(err))
                    
                except ChecksumError as err:
                    logger.log_event("error", str(err))
                    
                except OfflineError as err:
                    logger.log_event("critical", str(err))
                    logger.log_event("info", "Scanning aborted immediately.")
                    break 
                    
    except FileNotFoundError:
        logger.log_event("critical", "System Error: Input file missing.")

    logger.log_event("info", "\n=== Scan Complete. Review 'obd_diagnostics.txt' for background log details. ===")

if __name__ == "__main__":
    run_system_scan()