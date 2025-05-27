# def is_regular_graph():
#     # Read number of vertices
#     n = int(input("Enter number of vertices: "))
#
#     # Read adjacency matrix
#     print(f"Enter the {n}×{n} adjacency matrix, one row per line:")
#     adj = []
#     for _ in range(n):
#         row = list(map(int, input().split()))
#         if len(row) != n:
#             raise ValueError(f"Each row must have {n} entries")
#         adj.append(row)
#
#     # Compute degrees
#     degrees = [sum(row) for row in adj]
#
#     # Check regularity
#     if all(deg == degrees[0] for deg in degrees):
#         print("true")
#     else:
#         print("false")
#
#
# if __name__ == "__main__":
#     is_regular_graph()

file_path = 'input (6).txt'  # ← change this to your actual input filename


def is_regular_graph():
    with open(file_path, 'r') as f:
        n = int(f.readline().strip())

        adj = []
        for _ in range(n):
            row = list(map(int, f.readline().split()))
            if len(row) != n:
                raise ValueError(f"Expected {n} entries on each row, got {len(row)}")
            adj.append(row)

    degrees = [sum(row) for row in adj]

    if all(deg == degrees[0] for deg in degrees):
        print("true")
    else:
        print("false")


if __name__ == "__main__":
    is_regular_graph()

