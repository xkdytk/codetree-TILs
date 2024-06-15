def fix(turn):
    for y in range(N):
        for x in range(M):
            if info[y][x] > 0 and attack[y][x] != turn and not damage[y][x]:
                info[y][x] += 1
                
    return

def cannon(ay, ax, ty, tx):
    global num
    info[ty][tx] -= info[ay][ax]
    damage[ty][tx] = True
    if info[ty][tx] < 1:
        num -= 1

    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)):
        ny, nx = (ty+dy)%N, (tx+dx)%M

        if (ny, nx) != (ay, ax) and info[ny][nx] > 0:
            info[ny][nx] -= info[ay][ax]//2
            damage[ny][nx] = True
            if info[ny][nx] < 1:
                num -= 1

    return

def laser(ay, ax, ty, tx):
    global num
    stack = []
    stack.append((ay, ax, 0, []))
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[ay][ax] = True
    pos = []
    
    while stack:
        y, x, cnt, lst = stack.pop(0)
        if (y, x) == (ty, tx):
            pos = lst
            break

        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ny, nx = (y+dy)%N, (x+dx)%M

            # if ny < 0: ny = N-1
            # elif ny > N-1: ny = 0
            
            # if nx < 0: nx = N-1
            # elif nx > N-1: nx = 0
            # nx에는 N-1이 아니라 M-1이다.

            if not visited[ny][nx] and info[ny][nx] > 0:
                visited[ny][nx] = True
                nlst = lst[:]
                nlst.append((ny, nx))
                stack.append((ny, nx, cnt+1, nlst))
                # append 는 리스트에 항목을 추가한 후 None을 반환한다.  
                # 따라서 append를 호출한 결과를 직접 stack에 추가하지 않고, 먼저 새로운 리스트를 만들어 추가

    if len(pos) == 0:
        return False
    else:
        for i in range(len(pos)):
            ty, tx = pos[i]
            damage[ty][tx] = True
            if i == len(pos)-1:
                info[ty][tx] -= info[ay][ax]
            else:
                info[ty][tx] -= info[ay][ax]//2
            
            if info[ty][tx] < 1:
                num -= 1

        return True

def do_attack(ay, ax):
    power = 0
    candi = []
    for y in range(N):
        for x in range(M):
            if info[y][x] > 0 and (y, x) != (ay, ax):
                if power < info[y][x]:
                    power = info[y][x]
                    candi = [(attack[y][x], x+y, x, y)]
                elif power == info[y][x]:
                    candi.append((attack[y][x], x+y, x, y))

    candi.sort()
    dy, dx = candi[0][-1], candi[0][-2]

    if not laser(ay, ax, dy, dx):
        cannon(ay, ax, dy, dx)

def find_attacker(turn):
    power = 5001
    candi = []
    for y in range(N):
        for x in range(M):
            if info[y][x] > 0:
                if power > info[y][x]:
                    power = info[y][x]
                    candi = [(attack[y][x], x+y, x, y)]
                elif power == info[y][x]:
                    candi.append((attack[y][x], x+y, x, y))
    
    candi.sort(reverse=True)
    ay, ax = candi[0][-1], candi[0][-2]
    info[ay][ax] += N+M

    attack[ay][ax] = turn

    return ay, ax

N, M, K = map(int, input().split())
info = []
attack = [[0 for _ in range(M)] for _ in range(N)]
num = N*M

for _ in range(N):
    lst = list(map(int, input().split()))
    info.append(lst)
    num -= lst.count(0)

for turn in range(1, K+1):
    if num < 2: break
    damage = [[False for _ in range(M)] for _ in range(N)]
    ay, ax = find_attacker(turn)
    do_attack(ay, ax)
    fix(turn)

print(max(map(max, info)))