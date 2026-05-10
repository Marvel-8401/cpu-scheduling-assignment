"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: round_robin.py — Round Robin (default Time Quantum = 2)
============================================================

Algorithm:
  Processes are placed in a ready queue ordered by arrival
  time.  Each process is given a time slice (quantum).
  If it does not finish within the quantum it is preempted
  and moved to the back of the ready queue.
  Newly arrived processes are enqueued before the preempted
  process when they arrive at the exact moment of preemption.

Metrics:
  CT  = Completion Time  (last time the process leaves the CPU)
  TAT = Turnaround Time  = CT - AT
  WT  = Waiting Time     = TAT - BT
============================================================
"""

import copy
from collections import deque


def round_robin(processes, quantum=2):
    """
    Round Robin CPU scheduling.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: 'pid' (str), 'at' (int), 'bt' (int)
    quantum   : int
        CPU time slice per turn (default = 2)

    Returns
    -------
    list of dict
        Original fields plus 'ct', 'tat', 'wt' for each process.
    """
    # Sort a deep copy by arrival time (then PID) to establish initial order
    procs = sorted(copy.deepcopy(processes), key=lambda p: (p['at'], p['pid']))
    n     = len(procs)

    # Track remaining burst for each process
    remaining_bt = {p['pid']: p['bt'] for p in procs}
    proc_map     = {p['pid']: p        for p in procs}

    completion_time = {}   # pid -> CT
    ready_queue     = deque()
    current_time    = 0
    idx             = 0    # next process in arrival-sorted list to enqueue
    completed       = 0

    # Seed queue with the first process (or any arriving at time 0)
    while idx < n and procs[idx]['at'] <= current_time:
        ready_queue.append(procs[idx]['pid'])
        idx += 1

    # If no process arrives at 0, fast-forward
    if not ready_queue and idx < n:
        current_time = procs[idx]['at']
        while idx < n and procs[idx]['at'] <= current_time:
            ready_queue.append(procs[idx]['pid'])
            idx += 1

    while completed < n:
        if not ready_queue:
            # CPU idle — jump to next arrival
            current_time = procs[idx]['at']
            while idx < n and procs[idx]['at'] <= current_time:
                ready_queue.append(procs[idx]['pid'])
                idx += 1
            continue

        pid = ready_queue.popleft()
        run_time = min(quantum, remaining_bt[pid])

        # Execute for run_time units
        current_time += run_time
        remaining_bt[pid] -= run_time

        # Enqueue any processes that arrived during this time slice
        while idx < n and procs[idx]['at'] <= current_time:
            ready_queue.append(procs[idx]['pid'])
            idx += 1

        if remaining_bt[pid] == 0:
            # Process finished
            completion_time[pid] = current_time
            completed += 1
        else:
            # Re-queue the preempted process at the back
            ready_queue.append(pid)

    # Build output with full metrics
    output = []
    for p in procs:
        pid = p['pid']
        ct  = completion_time[pid]
        tat = ct - p['at']
        wt  = tat - p['bt']
        output.append({
            'pid': pid,
            'at' : p['at'],
            'bt' : p['bt'],
            'ct' : ct,
            'tat': tat,
            'wt' : wt,
        })

    return sorted(output, key=lambda p: p['pid'])


# ── Quick self-test ────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {"pid": "P1", "at": 0, "bt": 7},
        {"pid": "P2", "at": 2, "bt": 4},
        {"pid": "P3", "at": 4, "bt": 1},
        {"pid": "P4", "at": 5, "bt": 4},
    ]
    results = round_robin(sample, quantum=2)
    print(f"{'PID':<6} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<6} {'WT':<5}")
    for p in results:
        print(f"{p['pid']:<6} {p['at']:<5} {p['bt']:<5} {p['ct']:<5} {p['tat']:<6} {p['wt']:<5}")
    total_tat = sum(p['tat'] for p in results)
    total_wt  = sum(p['wt']  for p in results)
    n = len(results)
    print(f"\nAvg TAT = {total_tat/n:.2f}   Avg WT = {total_wt/n:.2f}")
