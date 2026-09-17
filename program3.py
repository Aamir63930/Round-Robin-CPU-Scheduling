# program3.py

# ---------------------------------------------------------
# PART 1: IMPORT AND INPUT DATA
# ---------------------------------------------------------

# deque is used for implementing the Ready Queue in
# Round Robin Scheduling
from collections import deque


# Process information
# AT = Arrival Time
# BT = Burst Time
# Priority: Smaller number means higher priority

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]


# ---------------------------------------------------------
# PART 2: NON-PREEMPTIVE PRIORITY SCHEDULING
# ---------------------------------------------------------

def priority_scheduling(processes):

    # Current CPU time
    current_time = 0

    # Set to store processes that have completed
    completed = set()

    # Stores final execution intervals
    result = []

    # Continue until all processes are completed
    while len(completed) < len(processes):

        # Find processes that have arrived
        # and are not completed yet
        ready = [
            p for p in processes
            if p["arrival"] <= current_time
            and p["pid"] not in completed
        ]

        # If no process is ready, CPU remains idle
        if not ready:

            # Find the next process arrival time
            next_time = min(
                p["arrival"]
                for p in processes
                if p["pid"] not in completed
            )

            # Store idle interval
            result.append(("IDLE", current_time, next_time))

            # Move current time to next arrival
            current_time = next_time

            continue

        # Select process with highest priority
        #
        # Smaller priority number = higher priority
        #
        # If priority is same:
        # 1. Earlier arrival time is selected
        # 2. PID is used as final tie-breaker
        p = min(
            ready,
            key=lambda x: (
                x["priority"],
                x["arrival"],
                x["pid"]
            )
        )

        # Starting time of selected process
        start = current_time

        # Ending time = start time + burst time
        end = start + p["burst"]

        # Store process execution interval
        result.append((p["pid"], start, end))

        # Update current time
        current_time = end

        # Mark process as completed
        completed.add(p["pid"])

    return result


# ---------------------------------------------------------
# PART 3: ROUND ROBIN SCHEDULING
# ---------------------------------------------------------

def round_robin(processes, quantum):

    # Quantum must be greater than 0
    if quantum <= 0:
        print("Quantum must be greater than 0")
        return []

    # Sort processes according to:
    # 1. Arrival time
    # 2. PID
    process_list = sorted(
        processes,
        key=lambda x: (
            x["arrival"],
            x["pid"]
        )
    )

    # Store remaining burst time of every process
    remaining = {
        p["pid"]: p["burst"]
        for p in process_list
    }

    # Ready Queue
    queue = deque()

    # Stores final execution intervals
    result = []

    # Current CPU time
    current_time = 0

    # Index of next process to be added
    i = 0

    # Continue while there are processes
    # that are not added OR queue is not empty
    while i < len(process_list) or queue:

        # If ready queue is empty
        if not queue:

            # If next process has not arrived yet,
            # CPU remains idle
            if current_time < process_list[i]["arrival"]:

                result.append(
                    (
                        "IDLE",
                        current_time,
                        process_list[i]["arrival"]
                    )
                )

                # Move time to process arrival
                current_time = process_list[i]["arrival"]

            # Add all processes that have arrived
            while (
                i < len(process_list)
                and process_list[i]["arrival"] <= current_time
            ):
                queue.append(process_list[i])
                i += 1

        # Take the first process from Ready Queue
        p = queue.popleft()

        # Process can execute for:
        # quantum OR remaining burst time,
        # whichever is smaller
        run_time = min(
            quantum,
            remaining[p["pid"]]
        )

        # Store start time
        start = current_time

        # Execute process
        current_time += run_time

        # Store execution interval
        result.append(
            (
                p["pid"],
                start,
                current_time
            )
        )

        # Decrease remaining burst time
        remaining[p["pid"]] -= run_time

        # Add newly arrived processes to Ready Queue
        while (
            i < len(process_list)
            and process_list[i]["arrival"] <= current_time
        ):
            queue.append(process_list[i])
            i += 1

        # If process is not completed,
        # put it back at the end of the queue
        if remaining[p["pid"]] > 0:
            queue.append(p)

    return result


# ---------------------------------------------------------
# PART 4: DISPLAY RESULT
# ---------------------------------------------------------

def show_result(title, result):

    # Print algorithm title
    print("\n" + title)

    # Print table heading
    print("Process Start End")

    # Print every execution interval
    for item in result:
        print(item[0], item[1], item[2])

    # Extract process names
    sequence = [
        item[0]
        for item in result
    ]

    # Display execution sequence
    print("Sequence:", " -> ".join(sequence))


# ---------------------------------------------------------
# DISPLAY INPUT DATA
# ---------------------------------------------------------

print("INPUT DATA")

print("PID AT BT Priority")

for p in processes:
    print(
        p["pid"],
        p["arrival"],
        p["burst"],
        p["priority"]
    )


# Priority rule
print("\nPriority Rule: Smaller number = Higher priority")


# ---------------------------------------------------------
# RUN NON-PREEMPTIVE PRIORITY SCHEDULING
# ---------------------------------------------------------

priority_result = priority_scheduling(processes)

show_result(
    "NON-PREEMPTIVE PRIORITY",
    priority_result
)


# ---------------------------------------------------------
# RUN ROUND ROBIN SCHEDULING
# ---------------------------------------------------------

# Time Quantum
quantum = 2

print("\nRound Robin Quantum =", quantum)

# Run Round Robin
rr_result = round_robin(
    processes,
    quantum
)

# Display Round Robin result
show_result(
    "ROUND ROBIN",
    rr_result
)