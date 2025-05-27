# def largest_connected_component():
#     import sys
#     sys.setrecursionlimit(1000000)
#
#     n, m = map(int, input().split())
#     adj = [[] for _ in range(n + 1)]
#     for _ in range(m):
#         u, v = map(int, input().split())
#         adj[u].append(v)
#         adj[v].append(u)
#
#     visited = [False] * (n + 1)
#
#     def dfs(start):
#         stack = [start]
#         visited[start] = True
#         size = 0
#         while stack:
#             u = stack.pop()
#             size += 1
#             for w in adj[u]:
#                 if not visited[w]:
#                     visited[w] = True
#                     stack.append(w)
#         return size
#
#     max_size = 0
#     for i in range(1, n + 1):
#         if not visited[i]:
#             max_size = max(max_size, dfs(i))
#
#     print(max_size)
#
#
# if __name__ == "__main__":
#     largest_connected_component()

file_path = 'input (5).txt'

def largest_connected_component():
    with open(file_path, 'r') as f:
        n, m = map(int, f.readline().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, f.readline().split())
            adj[u].append(v)
            adj[v].append(u)

    visited = [False] * (n + 1)

    def dfs(start):
        stack = [start]
        visited[start] = True
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            for w in adj[u]:
                if not visited[w]:
                    visited[w] = True
                    stack.append(w)
        return size

    max_size = 0
    for i in range(1, n + 1):
        if not visited[i]:
            max_size = max(max_size, dfs(i))

    print(max_size)


if __name__ == "__main__":
    largest_connected_component()

