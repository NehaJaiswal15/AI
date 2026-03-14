import time
import heapq
from collections import deque
import matplotlib.pyplot as plt

GRID = 10
START = (0,0)
GOAL = (9,9)

blocked = {(3,3),(3,4),(3,5),(4,5),(5,5)}

moves = [(1,0),(-1,0),(0,1),(0,-1)]

def neighbors(node):
    x,y = node
    for dx,dy in moves:
        nx,ny = x+dx, y+dy
        if 0 <= nx < GRID and 0 <= ny < GRID and (nx,ny) not in blocked:
            yield (nx,ny)

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def bfs():
    t0 = time.perf_counter()
    q = deque([START])
    visited = {START}
    count = 0

    while q:
        node = q.popleft()
        count += 1

        if node == GOAL:
            break

        for n in neighbors(node):
            if n not in visited:
                visited.add(n)
                q.append(n)

    return count, time.perf_counter() - t0

def dfs():
    t0 = time.perf_counter()
    stack = [START]
    visited = {START}
    count = 0

    while stack:
        node = stack.pop()
        count += 1

        if node == GOAL:
            break

        for n in neighbors(node):
            if n not in visited:
                visited.add(n)
                stack.append(n)

    return count, time.perf_counter() - t0

def bidirectional_bfs():
    t0 = time.perf_counter()

    q_start = deque([START])
    q_goal = deque([GOAL])

    visited_start = {START}
    visited_goal = {GOAL}

    explored = 0

    while q_start and q_goal:

        node_s = q_start.popleft()
        explored += 1

        for n in neighbors(node_s):
            if n in visited_goal:
                return explored, time.perf_counter() - t0
            if n not in visited_start:
                visited_start.add(n)
                q_start.append(n)

        node_g = q_goal.popleft()
        explored += 1

        for n in neighbors(node_g):
            if n in visited_start:
                return explored, time.perf_counter() - t0
            if n not in visited_goal:
                visited_goal.add(n)
                q_goal.append(n)

    return explored, time.perf_counter() - t0

def uniform_cost():
    t0 = time.perf_counter()

    pq = []
    heapq.heappush(pq,(0,START))

    visited=set()
    explored=0

    while pq:
        cost,node = heapq.heappop(pq)
        explored +=1

        if node == GOAL:
            break

        if node in visited:
            continue

        visited.add(node)

        for n in neighbors(node):
            heapq.heappush(pq,(cost+1,n))

    return explored, time.perf_counter() - t0

def best_first():
    t0 = time.perf_counter()

    pq=[]
    heapq.heappush(pq,(heuristic(START,GOAL),START))

    visited=set()
    explored=0

    while pq:
        h,node = heapq.heappop(pq)
        explored+=1

        if node == GOAL:
            break

        if node in visited:
            continue

        visited.add(node)

        for n in neighbors(node):
            heapq.heappush(pq,(heuristic(n,GOAL),n))

    return explored, time.perf_counter() - t0

def astar():
    t0 = time.perf_counter()

    pq=[]
    heapq.heappush(pq,(0,START))

    visited=set()
    explored=0

    while pq:
        cost,node = heapq.heappop(pq)
        explored+=1

        if node == GOAL:
            break

        if node in visited:
            continue

        visited.add(node)

        for n in neighbors(node):
            g = cost + 1
            f = g + heuristic(n,GOAL)
            heapq.heappush(pq,(f,n))

    return explored, time.perf_counter() - t0

print("\nSearch Algorithm Comparison\n")

results = {
    "BFS": bfs(),
    "DFS": dfs(),
    "Bi-BFS": bidirectional_bfs(),
    "UCS": uniform_cost(),
    "BestFS": best_first(),
    "A*": astar()
}

print("{:<10} {:<18} {:<12}".format("Algorithm","Nodes Explored","Time (sec)"))
print("-"*42)

algorithms = []
nodes_explored = []
execution_times = []

for algo,data in results.items():
    nodes,t = data

    print("{:<10} {:<18} {:<12.6f}".format(algo,nodes,t))

    algorithms.append(algo)
    nodes_explored.append(nodes)
    execution_times.append(t)

plt.figure()
plt.bar(algorithms, nodes_explored)

plt.title("Search Algorithm Comparison (Nodes Explored)")
plt.xlabel("Algorithms")
plt.ylabel("Nodes Explored")

plt.show()

plt.figure()
plt.bar(algorithms, execution_times)

plt.title("Search Algorithm Comparison (Execution Time)")
plt.xlabel("Algorithms")
plt.ylabel("Time (seconds)")

plt.show()