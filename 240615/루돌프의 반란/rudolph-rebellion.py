def inter(y, x, dir, id):
    nid = A[y][x]
    A[y][x] = id
    santa[id] = (y, x)
    
    ny, nx = y+dir[0], x+dir[1]
    if 0<=ny<N and 0<=nx<N:
        if A[ny][nx] != 0:
                inter(ny, nx, dir, nid)
        else:
            A[ny][nx] = nid
            santa[nid] = (ny, nx)
    
    else:
        fail[id] = True
    
    return    

def rmove(turn):
    global ry, rx
    dist = 2*(P**2)
    select = []
    for i in range(1, P+1):
        if not fail[i]:
            sy, sx = santa[i]
            nd = (ry-sy)**2 + (rx-sx)**2
            if nd < dist:
                dist = nd
                select = [(sy, sx, i)]
            elif nd == dist:
                select.append((sy, sx, i))
                
    select.sort(reverse=True)
    sy, sx, id = select[0]
    
    dist = (ry-sy)**2 + (rx-sx)**2
    dir = (0, 0)
    for d in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)):
        if 0<=ry+d[0]<N and 0<=rx+d[1]<N:
            nd = (ry+d[0]-sy)**2 + (rx+d[1]-sx)**2
            if nd < dist:
                dist = nd
                dir = d

    A[ry][rx] = 0
    ry, rx = ry+dir[0], rx+dir[1]   
    A[ry][rx] = -1  
    if (sy, sx) == (ry, rx):
        result[id] += C
        stun[id] = turn+2
        cy, cx = sy+dir[0]*C, sx+dir[1]*C
        santa[id] = (cy, cx)
        if 0<=cy<N and 0<=cx<N:
            if A[cy][cx] != 0:
                inter(cy, cx, dir, id)
            else:
                A[cy][cx] = id
        else:
            fail[id] = True
        
    return    

def smove(turn):
    for i in range(1, P+1):
        if stun[i] <= turn and not fail[i]:
            sy, sx = santa[i]
            dist = (ry-sy)**2 + (rx-sx)**2
            dir = (0, 0)
            for dy, dx in ((-1, 0), (0, 1), (1, 0,), (0, -1)):
                ny, nx = sy+dy, sx+dx
                if 0<=ny<N and 0<=nx<N and (A[ny][nx] == 0 or A[ny][nx] == -1):
                    nd = (ry-ny)**2 + (rx-nx)**2
                    if nd < dist:
                        dist = nd
                        dir = (dy, dx)
                        
            if dir == (0, 0):
                continue
            else:
                A[sy][sx] = 0
                sy, sx = sy+dir[0], sx+dir[1]  
                santa[i] = (sy, sx)
                if (sy, sx) == (ry, rx):
                    result[i] += D
                    stun[i] = turn+2
                    dir = (-dir[0], -dir[1])
                    cy, cx = sy+dir[0]*D, sx+dir[1]*D
                    santa[i] = (cy, cx)
                    if 0<=cy<N and 0<=cx<N:
                        if A[cy][cx] != 0:
                            inter(cy, cx, dir, i)
                        else:
                            A[cy][cx] = i
                    else:
                        fail[i] = True
                else:
                    A[sy][sx] = i
                    
    return
                
                
            

N, M, P, C, D = map(int, input().split())

A = [[0 for _ in range(N)] for _ in range(N)]

ry, rx = map(int, input().split())
ry, rx = ry-1, rx-1
A[ry][rx] = -1
santa = [(-1, -1) for _ in range(P+1)]
for _ in range(P):
    i, y, x = map(int, input().split())
    santa[i] = (y-1, x-1)
    A[y-1][x-1] = i
    

fail = [False for _ in range(P+1)]
fail[0] = True
stun = [0 for _ in range(P+1)]
result = [0 for _ in range(P+1)]

for turn in range(1, M+1):
    rmove(turn)
    smove(turn)
    if fail.count(True) == P+1:
        break
    for i in range(1, len(fail)):
        if not fail[i]:
            result[i] += 1
            
print(*result[1:])