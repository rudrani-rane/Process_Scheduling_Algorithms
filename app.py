from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# FCFS (First Come, First Serve)
def fcfs(burst_times, arrival_times):
    n = len(burst_times)
    waiting_time = [0] * n
    turn_around_time = [0] * n
    gantt_chart = []

    # Sort processes by arrival time
    processes = sorted(zip(arrival_times, burst_times, range(n)))
    sorted_arrival_times, sorted_burst_times, indices = zip(*processes)

    # Calculate waiting time, turn around time, and Gantt chart
    completion_time = 0
    for i in range(n):
        if completion_time < sorted_arrival_times[i]:
            completion_time = sorted_arrival_times[i]
        gantt_chart.append({
            'process': f'P{indices[i]}',
            'start': completion_time,
            'end': completion_time + sorted_burst_times[i]
        })
        waiting_time[indices[i]] = completion_time - sorted_arrival_times[i]
        completion_time += sorted_burst_times[i]
        turn_around_time[indices[i]] = waiting_time[indices[i]] + sorted_burst_times[i]

    return waiting_time, turn_around_time, gantt_chart

# SJF (Non-Preemptive)
def sjf(burst_times, arrival_times):
    n = len(burst_times)
    waiting_time = [0] * n
    turn_around_time = [0] * n
    gantt_chart = []

    # Sort processes by burst time (after arrival time)
    processes = sorted(zip(arrival_times, burst_times, range(n)))
    sorted_arrival_times, sorted_burst_times, indices = zip(*processes)

    # Scheduling logic
    completion_time = 0
    for i in range(n):
        available_processes = [
            (bt, idx) for at, bt, idx in zip(sorted_arrival_times, sorted_burst_times, indices)
            if at <= completion_time and waiting_time[idx] == 0
        ]
        if available_processes:
            next_process = min(available_processes)[1]
        else:
            completion_time = sorted_arrival_times[i]
            next_process = i
        gantt_chart.append({
            'process': f'P{indices[next_process]}',
            'start': completion_time,
            'end': completion_time + sorted_burst_times[next_process]
        })
        waiting_time[next_process] = max(completion_time - sorted_arrival_times[next_process], 0)
        completion_time += sorted_burst_times[next_process]
        turn_around_time[next_process] = waiting_time[next_process] + sorted_burst_times[next_process]

    return waiting_time, turn_around_time, gantt_chart

# Round Robin
def round_robin(burst_times, arrival_times, quantum):
    n = len(burst_times)
    remaining_burst = burst_times[:]
    waiting_time = [0] * n
    turn_around_time = [0] * n
    gantt_chart = []

    # Sort by arrival time
    processes = sorted(zip(arrival_times, burst_times, range(n)))
    sorted_arrival_times, sorted_burst_times, indices = zip(*processes)

    time = 0
    queue = [i for i in range(n) if sorted_arrival_times[i] <= time]

    while any(rb > 0 for rb in remaining_burst):
        for i in queue:
            if remaining_burst[i] > 0:
                gantt_chart.append({
                    'process': f'P{indices[i]}',
                    'start': time,
                    'end': time + min(quantum, remaining_burst[i])
                })
                if remaining_burst[i] > quantum:
                    time += quantum
                    remaining_burst[i] -= quantum
                else:
                    time += remaining_burst[i]
                    remaining_burst[i] = 0
                    waiting_time[indices[i]] = time - sorted_burst_times[i] - sorted_arrival_times[i]
                    turn_around_time[indices[i]] = waiting_time[indices[i]] + sorted_burst_times[i]
        queue = [i for i in range(n) if sorted_arrival_times[i] <= time and remaining_burst[i] > 0]

    return waiting_time, turn_around_time, gantt_chart

# Priority Scheduling (Non-Preemptive)
def priority_scheduling(burst_times, arrival_times, priorities):
    n = len(burst_times)
    waiting_time = [0] * n
    turn_around_time = [0] * n
    gantt_chart = []

    # Sort processes by priority (lower value = higher priority)
    processes = sorted(zip(arrival_times, burst_times, priorities, range(n)))
    sorted_arrival_times, sorted_burst_times, sorted_priorities, indices = zip(*processes)

    # Calculate waiting time, turn around time, and Gantt chart
    completion_time = 0
    for i in range(n):
        available_processes = [
            (priority, idx) for at, bt, priority, idx in zip(
                sorted_arrival_times, sorted_burst_times, sorted_priorities, indices
            ) if at <= completion_time and waiting_time[idx] == 0
        ]
        if available_processes:
            next_process = min(available_processes)[1]
        else:
            completion_time = sorted_arrival_times[i]
            next_process = i
        gantt_chart.append({
            'process': f'P{indices[next_process]}',
            'start': completion_time,
            'end': completion_time + sorted_burst_times[next_process]
        })
        waiting_time[next_process] = max(completion_time - sorted_arrival_times[next_process], 0)
        completion_time += sorted_burst_times[next_process]
        turn_around_time[next_process] = waiting_time[next_process] + sorted_burst_times[next_process]

    return waiting_time, turn_around_time, gantt_chart

# Flask routes to handle inputs
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    algorithm = data.get('algorithm')
    burst_times = data.get('burst_times')
    arrival_times = data.get('arrival_times')
    quantum = data.get('quantum', 1)
    priorities = data.get('priorities', [])

    if algorithm == 'FCFS':
        wt, tat, gantt_chart = fcfs(burst_times, arrival_times)
    elif algorithm == 'SJF':
        wt, tat, gantt_chart = sjf(burst_times, arrival_times)
    elif algorithm == 'Round Robin':
        wt, tat, gantt_chart = round_robin(burst_times, arrival_times, quantum)
    elif algorithm == 'Priority':
        wt, tat, gantt_chart = priority_scheduling(burst_times, arrival_times, priorities)
    else:
        return jsonify({'error': 'Invalid algorithm selected'})

    return jsonify({'waiting_time': wt, 'turnaround_time': tat, 'gantt_chart': gantt_chart})

if __name__ == "__main__":
    app.run(debug=True)

