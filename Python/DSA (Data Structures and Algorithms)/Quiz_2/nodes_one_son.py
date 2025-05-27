# # class TreeNode:
# #     def __init__(self, val):
# #         self.val = val
# #         self.left = None
# #         self.right = None
# #
# #
# # class BST:
# #     def __init__(self):
# #         self.root = None
# #
# #     def insert(self, val):
# #         if not self.root:
# #             self.root = TreeNode(val)
# #         else:
# #             self._insert(self.root, val)
# #
# #     def _insert(self, node, val):
# #         if val < node.val:
# #             if node.left:
# #                 self._insert(node.left, val)
# #             else:
# #                 node.left = TreeNode(val)
# #         else:
# #             if node.right:
# #                 self._insert(node.right, val)
# #             else:
# #                 node.right = TreeNode(val)
# #
# #     def count_single_child_nodes(self):
# #         return self._count_single_child_nodes(self.root)
# #
# #     def _count_single_child_nodes(self, node):
# #         if not node:
# #             return 0
# #
# #         count = 0
# #         if (node.left and not node.right) or (node.right and not node.left):
# #             count += 1
# #
# #         count += self._count_single_child_nodes(node.left)
# #         count += self._count_single_child_nodes(node.right)
# #
# #         return count
# #
# #
# # with open("tree.txt", "r") as file:
# #     values = list(map(int, file.readline().split()))
# #
# # bst = BST()
# # for val in values:
# #     bst.insert(val)
# #
# # print(bst.count_single_child_nodes())
# #
# # class Node:
# #     def __init__(self, v):
# #         self.v = v
# #         self.l = None
# #         self.r = None
# #
# # def insert(root, val):
# #     if root is None:
# #         return Node(val)
# #     if val < root.v:
# #         root.l = insert(root.l, val)
# #     elif val > root.v:
# #         root.r = insert(root.r, val)
# #     else:
# #         root.l = insert(root.l, val)
# #     return root
# #
# # def count_one_child(root):
# #     if root is None:
# #         return 0
# #     c = 1 if (root.l is None) ^ (root.r is None) else 0
# #     return c + count_one_child(root.l) + count_one_child(root.r)
# #
# # def main():
# #     with open("tree.txt") as f:
# #         vals = list(map(int, f.read().split()))
# #     root = None
# #     for v in vals:
# #         root = insert(root, v)
# #     res = count_one_child(root)
# #     print(res)
# #
# # if __name__ == "__main__":
# #     main()
#
# class Node:
#     def __init__(self, v):
#         self.v = v
#         self.l = None
#         self.r = None
#
# def insert(root, v):
#     if root is None:
#         return Node(v)
#     if v < root.v:
#         root.l = insert(root.l, v)
#     elif v > root.v:
#         root.r = insert(root.r, v)
#     else:
#         root.l = insert(root.l, v)
#     return root
#
# def count_one_child(root):
#     if root is None:
#         return 0
#     c = 1 if (root.l is None) ^ (root.r is None) else 0
#     return c + count_one_child(root.l) + count_one_child(root.r)
#
# nums = list(map(int, input().split()))
# root = None
# for v in nums:
#     root = insert(root, v)
# print(count_one_child(root))
#
#
#
#

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left:
                self._insert(node.left, val)
            else:
                node.left = TreeNode(val)
        else:
            if node.right:
                self._insert(node.right, val)
            else:
                node.right = TreeNode(val)

    def count_single_child_nodes(self):
        return self._count_single_child_nodes(self.root)

    def _count_single_child_nodes(self, node):
        if not node:
            return 0
        count = 0
        if (node.left and not node.right) or (node.right and not node.left):
            count += 1
        count += self._count_single_child_nodes(node.left)
        count += self._count_single_child_nodes(node.right)
        return count

values = list(map(int, input().split()))
bst = BST()
for val in values:
    bst.insert(val)

print(bst.count_single_child_nodes())