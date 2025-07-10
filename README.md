# 🧮 FCFS CPU Scheduling Simulation in Python  
**By Tahim Bhuiya**

This project implements a **First-Come, First-Served (FCFS) CPU Scheduling Algorithm** with support for **I/O bursts** in Python. It simulates the execution of processes with alternating CPU and I/O bursts, and computes performance metrics like **waiting time**, **turnaround time**, **response time**, and **CPU utilization**.

---

## 📜 Overview

This simulation models how an operating system schedules processes using the **FCFS non-preemptive algorithm**, where:

- Each process has a list of CPU bursts and I/O times  
- Processes execute their bursts in order  
- I/O-bound processes are temporarily removed from the ready queue  
- Time is advanced to simulate actual scheduling with idle gaps when needed  
- Metrics are tracked for all processes

---

## ▶️ Usage

Run the Python file directly:

```bash
python FCFS (Non-Preemptive) Scheduler.py
```

Then observe the simulation output in the terminal, including:

- Real-time status updates (e.g. which process is running or in I/O)  
- Completion logs for each process  
- A table with waiting, turnaround, and response times  
- CPU utilization and average performance metrics

---