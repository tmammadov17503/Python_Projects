class Node:
    def __init__(self,v):
        self.v=v
        self.l=None
        self.r=None

def insert(root,v):
    if not root:
        return Node(v)
    if v<root.v:
        root.l=insert(root.l,v)
    elif v>root.v:
        root.r=insert(root.r,v)
    return root

def find(root,x):
    if not root:
        return None
    if root.v==x:
        return root
    if x<root.v:
        return find(root.l,x)
    return find(root.r,x)

def invert(r):
    if r:
        r.l,r.r=r.r,r.l
        invert(r.l)
        invert(r.r)

def sum_right_leaves(root,is_right=False):
    if not root:
        return 0
    if not root.l and not root.r and is_right:
        return root.v
    return sum_right_leaves(root.l,False)+sum_right_leaves(root.r,True)

with open("tree (2).txt") as f:
    lines=f.read().splitlines()
arr=list(map(int,lines[0].split()))
x=int(lines[1])
root=None
for v in arr:
    root=insert(root,v)
r=find(root,x)
invert(r)
s=sum_right_leaves(root)
print(s)
