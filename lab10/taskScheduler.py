import heapq

tasks = {
    'A': {'duration': 3, 'deps': []},
    'B': {'duration': 2, 'deps': ['A']},
    'C': {'duration': 4, 'deps': ['A']},
    'D': {'duration': 3, 'deps': ['B', 'C']}
}

def heuristic(completed):
    remaining = [tasks[t]['duration'] for t in tasks if t not in completed]
    return sum(remaining)

def available_tasks(completed):
    avail = []
    for task in tasks:
        if task not in completed:
            if all(dep in completed for dep in tasks[task]['deps']):
                avail.append(task)
    return avail

def astar_scheduler():

    start = (0, [], 0)
    # (f_cost, completed_tasks, g_cost)

    pq = []
    heapq.heappush(pq, start)

    visited = set()

    while pq:
        f, completed, g = heapq.heappop(pq)

        completed_tuple = tuple(completed)

        if completed_tuple in visited:
            continue

        visited.add(completed_tuple)

        if len(completed) == len(tasks):
            return completed, g

        for task in available_tasks(completed):

            new_completed = completed + [task]
            new_cost = g + tasks[task]['duration']

            h = heuristic(new_completed)
            f_new = new_cost + h

            heapq.heappush(pq, (f_new, new_completed, new_cost))

def greedy_scheduler():

    completed = []
    total_time = 0

    while len(completed) < len(tasks):

        avail = available_tasks(completed)

        next_task = min(avail, key=lambda x: tasks[x]['duration'])

        completed.append(next_task)
        total_time += tasks[next_task]['duration']

    return completed, total_time

astar_order, astar_time = astar_scheduler()
greedy_order, greedy_time = greedy_scheduler()

print("A* Optimal Schedule:")
print("Order:", astar_order)
print("Total Time:", astar_time)

print("\nGreedy Schedule:")
print("Order:", greedy_order)
print("Total Time:", greedy_time)