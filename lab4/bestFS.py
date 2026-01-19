from heapq import heappush, heappop

def bestFirstSearch(edges, src, target, n):
    
    adj = [[] for _ in range(n)]
    for edge in edges:
        adj[edge[0]].append([edge[1], edge[2]])
        adj[edge[1]].append([edge[0], edge[2]])

    visited = [False] * n
    pq = []
    
    heappush(pq, [0, src])
    
    visited[src] = True   
    path = []
    
    while pq:
        x = heappop(pq)[1]
        path.append(x)
        
        if x == target:
            break
        
        for edge in adj[x]:
            if not visited[edge[0]]:
                visited[edge[0]] = True
                heappush(pq, [edge[1], edge[0]])
    
    return path

if __name__ == "__main__":
    n = 14
    edgeList = [
        [0, 1, 3], [0, 2, 6], [0, 3, 5],
        [1, 4, 9], [1, 5, 8], [2, 6, 12],
        [2, 7, 14], [3, 8, 7], [8, 9, 5],
        [8, 10, 6], [9, 11, 1], [9, 12, 10],
        [9, 13, 2]
    ]
    source = 0
    target = 9
    path = bestFirstSearch(edgeList, source, target, n)
    for i in range(len(path)):
        print(path[i], end=" ")