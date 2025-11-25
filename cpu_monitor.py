import time
import sys
import psutil

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
THRESHOLD = 80          # percent – raise an alert when CPU > this value
INTERVAL = 2            # seconds between checks (adjust as needed)

def monitor_cpu(threshold: int = THRESHOLD, interval: int = INTERVAL) -> None:
    """
    Continuously monitor CPU usage.
    Prints an alert whenever usage exceeds *threshold*.
    """
    print("Monitoring CPU usage... (press Ctrl+C to stop)")

    while True:
        try:
            # psutil.cpu_percent blocks for *interval* seconds and returns the
            # average CPU usage over that period.
            usage = psutil.cpu_percent(interval=interval)

            if usage > threshold:
                print(f"Alert! CPU usage exceeds threshold: {usage:.0f}%")
        except KeyboardInterrupt:
            # Graceful shutdown on user interrupt
            print("\nMonitoring stopped by user.")
            sys.exit(0)
        except Exception as exc:
            # Catch‑all for unexpected errors – log and continue
            print(f"Error while reading CPU stats: {exc}", file=sys.stderr)
            # Small pause before retrying to avoid tight error loops
            time.sleep(1)

if __name__ == "__main__":
    # You can also pass custom values via command‑line arguments if desired
    monitor_cpu()