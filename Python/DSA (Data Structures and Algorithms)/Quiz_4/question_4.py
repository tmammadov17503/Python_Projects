# import heapq
#
#
# def min_cost_route():
#     # Read number of cities
#     n = int(input("Enter number of cities: ").strip())
#
#     # Read gasoline costs
#     costs_list = list(map(int, input(f"Enter gasoline cost in each of the {n} cities (space-separated): ").split()))
#     if len(costs_list) != n:
#         raise ValueError(f"Expected {n} cost values, got {len(costs_list)}")
#     # 1-indexed
#     costs = [0] + costs_list
#
#     # Read roads
#     m = int(input("Enter number of roads: ").strip())
#     adj = [[] for _ in range(n + 1)]
#     print(f"Enter the {m} roads (each as two city indices u v):")
#     for _ in range(m):
#         u, v = map(int, input().split())
#         # assume 1 ≤ u,v ≤ n
#         adj[u].append(v)
#         adj[v].append(u)
#
#     # Dijkstra: distance[i] = min cost to reach city i
#     INF = 10 ** 18
#     distance = [INF] * (n + 1)
#     distance[1] = 0
#     heap = [(0, 1)]  # (cost_so_far, city)
#
#     while heap:
#         d, u = heapq.heappop(heap)
#         if d > distance[u]:
#             continue
#         for v in adj[u]:
#             # to go from u→v, spend one tank bought in city u
#             nd = d + costs[u]
#             if nd < distance[v]:
#                 distance[v] = nd
#                 heapq.heappush(heap, (nd, v))
#
#     # Output answer
#     ans = distance[n]
#     print(ans if ans < INF else -1)
#
#
# if __name__ == "__main__":
#     min_cost_route()


# file_path = '1(4).in.txt'  # ← change this to your actual input filename
#
# import heapq
#
# def min_cost_route():
#     # Read all tokens from the input file
#     with open(file_path, 'r') as f:
#         tokens = f.read().split()
#     it = iter(tokens)
#
#     # Number of cities
#     n = int(next(it))
#
#     # Gasoline costs (1-indexed)
#     costs = [0] + [int(next(it)) for _ in range(n)]
#
#     # Number of roads
#     m = int(next(it))
#
#     # Read 2*m integers for the edges
#     road_nums = [int(next(it)) for _ in range(2 * m)]
#
#     # Build adjacency list
#     adj = [[] for _ in range(n + 1)]
#     for i in range(m):
#         u = road_nums[2*i]
#         v = road_nums[2*i + 1]
#         if 1 <= u <= n and 1 <= v <= n:
#             adj[u].append(v)
#             adj[v].append(u)
#
#     # Dijkstra-like: distance[i] = min cost to reach city i
#     INF = 10**18
#     distance = [INF] * (n + 1)
#     distance[1] = 0
#     heap = [(0, 1)]  # (cost_so_far, city)
#
#     while heap:
#         d, u = heapq.heappop(heap)
#         if d > distance[u]:
#             continue
#         for v in adj[u]:
#             # moving from u to v costs costs[u]
#             nd = d + costs[u]
#             if nd < distance[v]:
#                 distance[v] = nd
#                 heapq.heappush(heap, (nd, v))
#
#     # Print result (or -1 if unreachable)
#     ans = distance[n]
#     print(ans if ans < INF else -1)
#
#
# if __name__ == "__main__":
#     min_cost_route()

import heapq

with open('1(4).in.txt') as f:
    data = f.read().split()
it = iter(data)

n = int(next(it))
costs = [0] + [int(next(it)) for _ in range(n)]
m = int(next(it))
roads = [(int(next(it)), int(next(it))) for _ in range(m)]

adj = [[] for _ in range(n+1)]
for u,v in roads:
    adj[u].append(v)
    adj[v].append(u)

INF = 10**18
dist = [INF]*(n+1)
dist[1] = 0
pq = [(0,1)]
while pq:
    d,u = heapq.heappop(pq)
    if d>dist[u]: continue
    for v in adj[u]:
        nd = d + costs[u]
        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(pq,(nd,v))

print(dist[n])
