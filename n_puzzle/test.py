from collections import deque
def dfs(idx,p):
    q = deque()
    q.append((idx,p))
    while q:
        idx,p = q.pop()
        D[idx] = D[p] + V[idx]
        for u in A[idx]:
            if u == p: continue
            q.append((u,idx))
