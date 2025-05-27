# def contains_cycle():
#     # 1) Read number of vertices
#     n = int(input().strip())
#
#     # 2) Build a deduplicated adjacency‐set (ignore self‐loops)
#     adj = {i: set() for i in range(1, n + 1)}
#     print("Enter edges u v, one per line. Ctrl+D (Unix)/Ctrl+Z (Win) to finish:")
#     while True:
#         try:
#             u, v = map(int, input().split())
#         except EOFError:
#             break
#         # ignore self‐loops
#         if u == v:
#             continue
#         adj[u].add(v)
#         adj[v].add(u)
#
#     visited = [False] * (n + 1)
#
#     def dfs(u, parent):
#         visited[u] = True
#         for w in adj[u]:
#             if not visited[w]:
#                 if dfs(w, u):
#                     return True
#             elif w != parent:
#                 # found an edge to a previously‐visited non‐parent ⇒ a simple cycle
#                 return True
#         return False
#
#     # 3) Run DFS from each component
#     for vertex in range(1, n + 1):
#         if not visited[vertex]:
#             if dfs(vertex, -1):
#                 print(1)
#                 return
#
#     # no cycle found
#     print(0)
#
#
# if __name__ == "__main__":
#     contains_cycle()


file_path = 'input (7).txt'


def contains_cycle():
    with open(file_path, 'r') as f:
        first = f.readline()
        if not first:
            print(0)
            return
        n = int(first.strip())

        adj = {i: set() for i in range(1, n + 1)}
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            u, v = map(int, parts)
            if u == v or not (1 <= u <= n and 1 <= v <= n):
                continue
            adj[u].add(v)
            adj[v].add(u)

    visited = [False] * (n + 1)

    def dfs(u, parent):
        visited[u] = True
        for w in adj[u]:
            if not visited[w]:
                if dfs(w, u):
                    return True
            elif w != parent:
                return True
        return False

    for vertex in range(1, n + 1):
        if not visited[vertex]:
            if dfs(vertex, -1):
                print(1)
                return

    print(0)


if __name__ == "__main__":
    contains_cycle()
