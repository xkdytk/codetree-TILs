def inter(py, px, dy, dx):
    pid = A[py][px]
    stack = [(py, px, pid)]
    
    while stack:
        py, px, pid = stack.pop(0)
        npy, npx = py+dy, px+dx
        if 0<=npy<N and 0<=npx<N:
            if A[npy][npx] != 0:
                stack.append((npy, npx, A[npy][npx]))
            A[npy][npx] = pid
            santa[pid] = (npy, npx)
        else:
            fail[pid] = True
    
    return
    

def r_move(r_pos, c, turn):
    ry, rx = r_pos
    near = []
    dist = 3*N**2
    
    for i in range(1, len(santa)):
        if not fail[i]:
            now = (ry-santa[i][0])**2 + (rx-santa[i][1])**2
            if dist > now:
                dist = now
                near = [(santa[i][0], santa[i][1], i)]
            elif dist == now:
                near.append((santa[i][0], santa[i][1], i))
    
    near = sorted(near, reverse=True)
    sy, sx, id = near[0]
    
    dy, dx = 0, 0
    if sy > ry: dy = 1
    elif sy < ry: dy = -1
    
    if sx > rx: dx = 1
    elif sx < rx: dx = -1
        
    A[ry][rx] = 0
    nry, nrx = ry+dy, rx+dx
    A[nry][nrx] = -1
    if (nry, nrx) == (sy, sx):
        result[id] += c
        stun[id] = turn + 2
        py, px = sy+c*dy, sx+c*dx
        santa[id] = (py, px)
        if 0<=py<N and 0<=px<N:
            if A[py][px] != 0:
                inter(py, px, dy, dx)
            A[py][px] = id
        else:
            fail[id] = True
            
    return (nry, nrx)

def s_move(r_pos, d, turn):
    ry, rx = r_pos
    for i in range(1, len(santa)):
        sy, sx = santa[i][0], santa[i][1]
        if not fail[i]:
            if stun[i] > turn:
                continue
            else:
                tlst = []
                dist = (ry-sy)**2 + (rx-sx)**2
                for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1)): # 거리 리스트로 관리하면 편함
                    nsy, nsx = sy+dy, sx+dx
                    if 0<=nsy<N and 0<=nsx<N and A[nsy][nsx] <= 0:
                        now = (ry-nsy)**2 + (rx-nsx)**2
                        if dist > now:
                            dist = now
                            tlst = [(nsy, nsx, dy, dx)]
                            
                if len(tlst) == 0: continue
                else:
                    A[sy][sx] = 0
                    nsy, nsx, dy, dx = tlst[0]
                    if (nsy, nsx) == (ry, rx):
                        dy, dx = -dy, -dx
                        result[i] += d
                        stun[i] = turn + 2
                        py, px = nsy+d*dy, nsx+d*dx
                        santa[i] = (py, px)
                        if 0<=py<N and 0<=px<N:
                            if A[py][px] != 0:
                                inter(py, px, dy, dx)
                            A[py][px] = i
                        else:
                            fail[i] = True
                    else:
                        santa[i] = (nsy, nsx)
                        A[nsy][nsx] = i
       
def end_check():
    if fail.count(True) == P+1:
        return True
def plus():
    for id in range(1, len(santa)):
        if not fail[id]:
            result[id] += 1
                
N, M, P, C, D = map(int, input().split())
r_y, r_x = map(int, input().split())
r_pos = (r_y-1, r_x-1) # 줄여서 편한것은 줄이고 원래 값을 유지해야하는 것은 유지 (이후에 헷갈리지 않도록 주의)

santa = [(0,0) for _ in range(P+1)]
stun = [1 for _ in range(P+1)]
fail = [False for _ in range(P+1)]
fail[0] = True

A = [[0 for _ in range(N)] for _ in range(N)]
A[r_pos[0]][r_pos[1]] = -1
for _ in range(P):
    num, y, x = map(int, input().split())
    santa[num] = (y-1, x-1)
    A[y-1][x-1] = num
    
result = [0 for _ in range(P+1)]
for turn in range(1, M+1):
    if end_check():
        break
    r_pos = r_move(r_pos, C, turn)
    s_move(r_pos, D, turn)
    plus()
    
print(*result[1:])