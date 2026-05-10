"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: fcfs.py — First Come First Served (Non-Preemptive)
============================================================

Algorithm:
  Processes are executed in order of their arrival time.
  Ties in arrival time are broken by process ID order.

Metrics:
  CT  = Completion Time
  TAT = Turnaround Time = CT - AT
  WT  = Waiting Time    = TAT - BT
============================================================
"""

import copy


def fcfs(processes):
    """
    First Come First Served scheduling.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: 'pid' (str), 'at' (int), 'bt' (int)

    Returns
    -------
    list of dict
        Original fields plus 'ct', 'tat', 'wt' for each process.
    """
    # Work on a sorted copy so we don't mutate the caller's data
    procs = sorted(copy.deepcopy(processes), key=lambda p: (p['at'], p['pid']))

    current_time = 0

    for p in procs:
        # If CPU is idle, jump to the arrival of the next process
        if current_time < p['at']:
            current_time = p['at']

        # Process runs to completion (non-preemptive)
        current_time += p['bt']

        p['ct']  = current_time
        p['tat'] = p['ct'] - p['at']
        p['wt']  = p['tat'] - p['bt']

    # Return results ordered by original process ID for consistent reporting
    return sorted(procs, key=lambda p: p['pid'])


# ── Quick self-test ────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {"pid": "P1", "at": 0, "bt": 7},
        {"pid": "P2", "at": 2, "bt": 4},
        {"pid": "P3", "at": 4, "bt": 1},
        {"pid": "P4", "at": 5, "bt": 4},
    ]
    results = fcfs(sample)
    print(f"{'PID':<6} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<6} {'WT':<5}")
    for p in results:
        print(f"{p['pid']:<6} {p['at']:<5} {p['bt']:<5} {p['ct']:<5} {p['tat']:<6} {p['wt']:<5}")
    total_tat = sum(p['tat'] for p in results)
    total_wt  = sum(p['wt']  for p in results)
    n = len(results)
    print(f"\nAvg TAT = {total_tat/n:.2f}   Avg WT = {total_wt/n:.2f}")
