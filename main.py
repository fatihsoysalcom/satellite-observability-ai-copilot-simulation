import random
import time

class Satellite:
    def __init__(self, name="Sat-001"):
        self.name = name
        self.power = 100.0  # Percentage
        self.temperature = 25.0  # Celsius
        self.data_buffer = 0  # MB
        self.status = "NOMINAL"
        self.max_data_buffer = 500
        self.max_power = 100.0
        self.min_power_threshold = 20.0
        self.max_temp_threshold = 40.0

    def _update_state(self):
        # Simulate power consumption
        self.power -= random.uniform(1.0, 5.0)
        self.power = max(0.0, self.power)

        # Simulate temperature fluctuation
        temp_change = random.uniform(-2.0, 3.0)
        if self.power < self.min_power_threshold: # Low power might mean less cooling
            temp_change += 1.0
        self.temperature += temp_change
        self.temperature = max(-50.0, min(100.0, self.temperature)) # Realistic bounds

        # Simulate data generation
        self.data_buffer += random.randint(10, 50)
        self.data_buffer = min(self.max_data_buffer, self.data_buffer)

        # Update status based on internal state
        if self.power < self.min_power_threshold:
            self.status = "LOW_POWER"
        elif self.temperature > self.max_temp_threshold:
            self.status = "OVERHEAT"
        elif self.data_buffer >= self.max_data_buffer * 0.9:
            self.status = "DATA_FULL"
        else:
            self.status = "NOMINAL"

    def operate(self):
        self._update_state()
        logs = []
        # Observability: Exposing internal state as structured metrics
        metrics = {
            "power": round(self.power, 2),
            "temperature": round(self.temperature, 2),
            "data_buffer": self.data_buffer,
            "status": self.status
        }

        # Observability: Generating event logs for contextual information
        if self.power < self.min_power_threshold + 5 and self.power > self.min_power_threshold:
            logs.append(f"[{self.name}] Power getting low: {self.power:.2f}%")
        if self.power < self.min_power_threshold:
            logs.append(f"[{self.name}] CRITICAL: Power below {self.min_power_threshold}%! Current: {self.power:.2f}%")
        if self.temperature > self.max_temp_threshold - 5 and self.temperature < self.max_temp_threshold:
            logs.append(f"[{self.name}] Temperature rising: {self.temperature:.2f}°C")
        if self.temperature > self.max_temp_threshold:
            logs.append(f"[{self.name}] WARNING: Overheat detected! Current: {self.temperature:.2f}°C")
        if self.data_buffer >= self.max_data_buffer * 0.9:
            logs.append(f"[{self.name}] Data buffer nearly full: {self.data_buffer}MB")
        if self.status == "NOMINAL" and not logs:
            logs.append(f"[{self.name}] Operating nominally.")

        return metrics, logs

    def apply_action(self, action):
        if action == "RECHARGE_POWER":
            self.power = min(self.max_power, self.power + random.uniform(10.0, 20.0))
            return f"[{self.name}] Action: Power recharged to {self.power:.2f}%."
        elif action == "COOL_DOWN":
            self.temperature = max(-50.0, self.temperature - random.uniform(5.0, 10.0))
            return f"[{self.name}] Action: Cooling initiated. Temp: {self.temperature:.2f}°C."
        elif action == "TRANSMIT_DATA":
            transmitted = random.randint(self.data_buffer // 2, self.data_buffer) if self.data_buffer > 0 else 0
            self.data_buffer -= transmitted
            self.data_buffer = max(0, self.data_buffer)
            return f"[{self.name}] Action: {transmitted}MB data transmitted. Buffer: {self.data_buffer}MB."
        elif action == "NO_ACTION":
            return f"[{self.name}] Action: No specific action needed."
        return f"[{self.name}] Unknown action: {action}"


class AICopilot:
    def __init__(self, satellite_name="Sat-001"):
        self.satellite_name = satellite_name
        self.power_threshold = 25.0 # Critical power level for action
        self.temp_threshold = 38.0  # Critical temperature level for action
        self.data_buffer_threshold_percent = 80 # Critical data buffer level for action

    def suggest_action(self, metrics, logs):
        # This is where the "AI" (simple rule-based logic) observes and decides.
        # It uses metrics and logs to infer the system's internal state and suggest actions.

        # Observability in action: Prioritize critical issues based on structured metrics
        if metrics["power"] < self.power_threshold:
            return "RECHARGE_POWER"
        if metrics["temperature"] > self.temp_threshold:
            return "COOL_DOWN"
        if metrics["data_buffer"] >= (satellite.max_data_buffer * self.data_buffer_threshold_percent / 100):
            return "TRANSMIT_DATA"

        # Observability in action: Check for specific log messages (less structured but valuable context)
        for log in logs:
            if "CRITICAL: Power" in log:
                return "RECHARGE_POWER"
            if "WARNING: Overheat" in log:
                return "COOL_DOWN"
            if "Data buffer nearly full" in log:
                return "TRANSMIT_DATA"

        return "NO_ACTION"

# --- Simulation --- 
if __name__ == "__main__":
    satellite = Satellite("Orbital-Eye-1")
    copilot = AICopilot("Orbital-Eye-1")

    print("--- AI-Supported Satellite Operations Simulation ---")
    print("Monitoring 'Orbital-Eye-1' with an AI Copilot for observability.")
    print("-" * 60)

    for i in range(1, 16): # Simulate 15 time steps
        print(f"\n--- Time Step {i} ---")

        # Satellite operates and generates observability data
        current_metrics, current_logs = satellite.operate()
        print(f"[{satellite.name}] Current Metrics: {current_metrics}")
        for log in current_logs:
            print(f"[{satellite.name}] Log: {log}")

        # AI Copilot observes the metrics and logs
        # This is the core observability loop: data -> inference -> action
        suggested_action = copilot.suggest_action(current_metrics, current_logs)
        print(f"[AI Copilot] Suggested Action: {suggested_action}")

        # Satellite applies the suggested action
        action_result = satellite.apply_action(suggested_action)
        print(action_result)

        time.sleep(0.5) # Pause for readability

    print("\n--- Simulation End ---")
