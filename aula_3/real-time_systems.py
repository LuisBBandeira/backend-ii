
import threading
import random
import time
from queue import Queue
from typing import Dict, Any, TypedDict

class SensorData(TypedDict):
    sensor: str
    value: float
    unit: str
    timestamp: str

data_queue: Queue[SensorData] = Queue()

sensors: Dict[str, Dict[str, Any]] = {
    "temperature": {"unit": "°C", "range": (-10, 50)},
    "motion": {"unit": "detections/sec", "range": (0, 100)},
    "pressure": {"unit": "kPa", "range": (80, 120)}
}

def sensor_thread(sensor_name: str, interval: float = 1) -> None:
    while True:
        min_val, max_val = sensors[sensor_name]["range"]
        value = random.uniform(min_val, max_val)
        timestamp = time.strftime("%H:%M:%S")

        data_queue.put({
            "sensor": sensor_name,
            "value": round(value, 2),
            "unit": sensors[sensor_name]["unit"],
            "timestamp": timestamp
        })
        
        time.sleep(interval)

def aggregation_thread() -> None:
    while True:
        if not data_queue.empty():
            data: SensorData = data_queue.get()
            
            print(
                f"[{data['timestamp']}] {data['sensor']}: {data['value']} {data['unit']}",
                end=""
            )

            if data["sensor"] == "temperature" and data["value"] > 40:
                print("   HIGH TEMP ALERT!", end="")
            elif data["sensor"] == "pressure" and data["value"] > 110:
                print("   HIGH PRESSURE!", end="")
            
            print()  
        
        time.sleep(0.1)  

if __name__ == "__main__":
    print("=== Starting Real-Time Sensor Simulation ===")

    for sensor in sensors:
        thread = threading.Thread(
            target=sensor_thread,
            args=(sensor,),
            daemon=True  
        )
        thread.start()
    
    threading.Thread(target=aggregation_thread, daemon=True).start()
    
    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nStopping simulation...")