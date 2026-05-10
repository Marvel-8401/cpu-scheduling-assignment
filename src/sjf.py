"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: sjf.py — Non-Preemptive Shortest Job First
============================================================

Algorithm:
  At each scheduling decision point (CPU becomes free),
  among all processes that have arrived, pick the one with
  the shortest burst time.  Ties are broken by arrival time,
  then by PID.  Once a process starts it runs to completion.

Metrics:
  CT  = Completion Time
  TAT = Turnaround Time = CT - AT
  WT  = Waiting Time    = TAT - BT
============================================================
"""

import copy


def sjf_non_preemptive(processes):
    """
    Non-Preemptive Shortest Job First scheduling.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: 'pid' (str), 'at' (int), 'bt' (int)

    Returns
    -------
    list of dict
        Original fields plus 'ct', 'tat', 'wt' for each process.
    """
    procs       = copy.deepcopy(processes)
    n           = len(procs)
    completed   = []          # finished processes (with metrics)
    remaining   = list(procs) # processes not yet scheduled
    current_time = 0

    while remaining:
        # Collect all processes that have arrived by current_time
        available = [p for p in remaining if p['at'] <= current_time]

        if not available:
            # CPU is idle — advance time to next arrival
            current_time = min(p['at'] for p in remaining)
            continue

        # Pick the process with shortest burst; break ties by AT then PID
        chosen = min(available, key=lambda p: (p['bt'], p['at'], p['pid']))
        remaining.remove(chosen)

        # Run chosen process to completion
        current_time += chosen['bt']

        chosen['ct']  = current_time
        chosen['tat'] = chosen['ct'] - chosen['at']
        chosen['wt']  = chosen['tat'] - chosen['bt']
        completed.append(chosen)

    # Return sorted by PID for consistent reporting
    return sorted(completed, key=lambda p: p['pid'])


# ── Quick self-test ────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {"pid": "P1", "at": 0, "bt": 7},
        {"pid": "P2", "at": 2, "bt": 4},
        {"pid": "P3", "at": 4, "bt": 1},
        {"pid": "P4", "at": 5, "bt": 4},
    ]
    results = sjf_non_preemptive(sample)
    print(f"{'PID':<6} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<6} {'WT':<5}")
    for p in results:
        print(f"{p['pid']:<6} {p['at']:<5} {p['bt']:<5} {p['ct']:<5} {p['tat']:<6} {p['wt']:<5}")
    total_tat = sum(p['tat'] for p in results)
    total_wt  = sum(p['wt']  for p in results)
    n = len(results)
    print(f"\nAvg TAT = {total_tat/n:.2f}   Avg WT = {total_wt/n:.2f}")
