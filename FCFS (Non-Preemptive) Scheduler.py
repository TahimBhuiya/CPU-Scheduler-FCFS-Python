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