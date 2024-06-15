DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]

def golem_move(r, c):
    global result
    stack = [(r, c)]
    visited = [[False for _ in range(C)] for _ in range(R+3)]
    visited[r][c] = True
    maxr = 0
    
    while stack:
        r, c = stack.pop(0)
        
        for i in range(4):
            nr, nc = r+DY[i], c+DX[i]
            if 0<=nr<R+3 and 0<=nc<C and not visited[nr][nc] and M[nr][nc] != 0:
                if M[nr][nc] == M[r][c]:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
                    maxr = max(nr, maxr)
                else:
                    if is_exit[r][c]:
                        visited[nr][nc] = True
                        stack.append((nr, nc))
                        maxr = max(nr, maxr)
                    
    result += maxr-2
    return

def move(c, d, id):
    global M, is_exit
    stack = [(1, c, d)]
    
    while stack:
        r, c, d = stack.pop()
        if r+2 < R+3 and M[r+1][c-1] == 0 and M[r+2][c] == 0 and M[r+1][c+1] == 0:
            stack.append((r+1, c, d))
            
        elif r+2 < R+3 and c-2 > -1 and M[r][c-2] == 0 and M[r-1][c-1] == 0 and M[r+1][c-1] == 0 and M[r+2][c-1] == 0 and M[r+1][c-2] == 0:
            # 반시계 회전
            d = (d-1)%4
            stack.append((r+1, c-1, d))
        
        elif r+2 < R+3 and c+2 < C and M[r][c+2] == 0 and M[r-1][c+1] == 0 and M[r+1][c+1] == 0 and M[r+2][c+1] == 0 and M[r+1][c+2] == 0:
            d = (d+1)%4
            stack.append((r+1, c+1, d))
        
    M[r][c] = id 
    for i in range(4):
        if i == d:
            is_exit[r+DY[i]][c+DX[i]] = True
        
        M[r+DY[i]][c+DX[i]] = id
    
    if r < 4:
        M = [[0 for _ in range(C)] for _ in range(R+3)]
        is_exit = [[False for _ in range(C)] for _ in range(R+3)]
        return
    else:
        golem_move(r, c)
        return
    
R, C, K = map(int, input().split())
M = [[0 for _ in range(C)] for _ in range(R+3)]
is_exit = [[False for _ in range(C)] for _ in range(R+3)]
result = 0

for id in range(1, K+1):
    c, d = map(int, input().split())
    move(c-1, d, id)
    
print(result)

# 모델을 돌려보고 디버그도 해봤는데 틀린 케이스가 나온다면 전체적으로 따라가면서 빠진 조건이나 잘못 적은 변수가 있는지 확인하자