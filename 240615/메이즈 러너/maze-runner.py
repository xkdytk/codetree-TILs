DX = [0, 0, -1, 1]
DY = [-1, 1, 0, 0]

def rotate():
    global ey, ex
    sq_size = N-1
    for y, x in people:
        sq_size = min(max(abs(y-ey), abs(x-ex)), sq_size)

    # 여기서 sq size를 하나 적게 구했는데 이러니까 헷갈린다.
    # 딱히 방법이 떠오르지 않으면 우선 완전 탐색을 생각하자. 완전 탐색 안에서 어떻게 더 효율적일지 구상
    sqy, sqx = 0, 0
    pos = False
    for y in range(N-sq_size):
        for x in range(N-sq_size):
            if y<=ey<=y+sq_size and x<=ex<=x+sq_size:
                for py, px in people:
                    if y<=py<=y+sq_size and x<=px<=x+sq_size:
                        sqy, sqx = y, x
                        pos = True
                        break
            if pos:
                break
        if pos:
            break
        
    tmp = [[0 for _ in range(N)] for _ in range(N)]
    p_tmp = [(-1, -1) for _ in range(len(people))]
    e_tmp = (-1, -1)
    
    for y in range(sqy, sqy+sq_size+1):
        for x in range(sqx, sqx+sq_size+1):
            if miro[y][x] != 0:
                miro[y][x] -= 1
            oy, ox = y-sqy, x-sqx
            ry, rx = ox, sq_size-oy
            tmp[sqy+ry][sqx+rx] = miro[y][x]
            if (y, x) == (ey, ex):
                e_tmp = (sqy+ry, sqx+rx)
            for i in range(len(people)):
                py, px = people[i]
                if (y, x) == (py, px):
                    p_tmp[i] = (sqy+ry, sqx+rx)
                    
    if e_tmp != (-1, -1):
        ey, ex = e_tmp
        
    for i in range(len(p_tmp)):
        if p_tmp[i] != (-1, -1):
            people[i] = p_tmp[i]

    for y in range(sqy, sqy+sq_size+1):
        for x in range(sqx, sqx+sq_size+1):
            miro[y][x] = tmp[y][x]

    return
                

def move():
    global ey, ex, mdist, people
    for i in range(len(people)):
        y, x = people[i]
        dist = abs(y-ey) + abs(x-ex)
        dir = -1
        for j in range(4):
            ny, nx = y+DY[j], x+DX[j]
            if 0<=ny<N and 0<=nx<N and (miro[ny][nx] == 0):
                now = abs(ny-ey) + abs(nx-ex)
                if dist > now:
                    dir = j
                    dist = now
                
        if dist == abs(y-ey) + abs(x-ex): continue
        else:
            ny, nx = y+DY[dir], x+DX[dir]
            mdist += 1
            if (ny, nx) == (ey, ex):
                people[i] = (-1, -1)
            else:
                people[i] = (ny, nx)

    # rm_lst를 만들어서 pop 하는건 위험함(ex 여러개의 제거값이 있을 때 하나씩 없애기 때문에 index 에러 발생)
    people = [(y, x) for y, x in people if (y, x) != (-1, -1)]
    return

N, M, K = map(int, input().split())
miro = []
for _ in range(N):
    miro.append(list(map(int, input().split())))

people = []
for _ in range(M):
    y, x = map(int, input().split())
    people.append((y-1, x-1))

ey, ex = map(int, input().split())
ey, ex = ey-1, ex-1
mdist = 0

for sec in range(1, K+1):
    if len(people) == 0: break
    move()
    if len(people) == 0: break
    rotate()

print(mdist)
print(ey+1, ex+1)

# 동시에 or 회전 라는 말이 나오면 리스트를 복사해서 사용