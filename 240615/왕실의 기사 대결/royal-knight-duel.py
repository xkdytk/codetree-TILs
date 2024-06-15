DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]

def check_move(id, dir):
    stack = []
    pos_move = True
    stack.append(id)
    id_lst = []
    id_lst.append(id)
    # 일단 주어진 것 stack에 넣는 방향으로 생각하자 너무 복잡하게 뭘해서 집어넣으려고 하지말고

    while stack:
        id = stack.pop()
        for y, x in knight[id]:
            ny, nx = y+DY[dir], x+DX[dir]
            if 0<=ny<L and 0<=nx<L:
                if chess[ny][nx] == 2:
                    pos_move = False
                    break
                elif k_map[ny][nx] != 0 and k_map[y][x] != k_map[ny][nx] and k_map[ny][nx] not in id_lst:
                    stack.append(k_map[ny][nx])
                    id_lst.append(k_map[ny][nx])
                    # (메모리 에러) for문 또는 bfs에서 append할 때 중복되는 것이 계속 저장되는지 확인 필수
            else:
                pos_move = False
                break

    return pos_move, id_lst    

def move(id, dir):
    if not remove[id]:
        pos_move, id_lst = check_move(id, dir)

        if pos_move:
            for i in id_lst:
                for y, x in knight[i]:
                    k_map[y][x] = 0
                    
            for i in id_lst:
                for j in range(len(knight[i])):
                    y, x = knight[i][j]
                    ny, nx = y+DY[dir], x+DX[dir]
                    knight[i][j] = (ny, nx)
                    k_map[ny][nx] = i
                    
            for i in id_lst:
                if id != i:
                    for y, x in knight[i]:
                        if chess[y][x] == 1:
                            hp[i] -= 1 
                            damages[i] += 1
                            
            for i in id_lst:
                if hp[i] <= 0:
                    remove[i] = True
                    damages[i] = 0
                    for y, x in knight[i]:
                        k_map[y][x] = 0
                        
            # for 문 한개로 처리하려고 노력하지 말고 나눠서 하자. 어차피 시간 남는다.
                    
    return

L, N, Q = map(int, input().split())
chess = []
for _ in range(L):
    chess.append(list(map(int, input().split())))

k_map = [[0 for _ in range(L)] for _ in range(L)]
knight = [[] for _ in range(N+1)]
hp = [0 for _ in range(N+1)]
remove = [False for _ in range(N+1)]
remove[0] = True
damages = [0 for _ in range(N+1)]
for id in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    hp[id] = k
    for y in range(r-1, r-1+h-1+1):
        for x in range(c-1, c-1+w-1+1):
            knight[id].append((y, x))
            k_map[y][x] = id

commend = []
for _ in range(Q):
    i, d = map(int, input().split())
    commend.append((i, d))

for i, d in commend:
    move(i, d)

print(sum(damages))

# 틀리면 당황하지말고 주어진 예제를 완벽하게 디버깅하자
# 예제 그림을 보이는대로 최대한 구현하려고 노력하자