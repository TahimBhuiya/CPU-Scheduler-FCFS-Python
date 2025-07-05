from collections import deque

# Define Process class to store process data
class Process:
    def __init__(self, pid, burst_times, io_times):
        self.pid = pid
        self.burst_times = burst_times  
        self.io_times = io_times       
        self.current_burst = 0          
        self.waiting_time = 0          
        self.turnaround_time = 0        
        self.response_time = -1         
        self.last_end_time = 0         
        
    def is_completed(self):
        return self.current_burst >= len(self.burst_times)

# Display simulation status
def display_status(current_time, running_process, ready_queue, io_list):
    print(f"\nCurrent Execution Time: {current_time}")
    if running_process:
        print(f"Running Process: P{running_process.pid}")
    else:
        print("Running Process: None")
    print("Ready Queue:", [(p.pid, p.burst_times[p.current_burst]) for p in ready_queue])
    print("Processes in I/O:", [(p.pid, t - current_time) for p, t in io_list])