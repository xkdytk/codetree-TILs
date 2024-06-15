def move():
    tmp = [() for _ in range(m+1)]
    for i in range(1, m+1):
        if arival[i] == 0 and len(people[i]) != 0:
            y, x = people[i]
            stack = [(y, x, [])]
            
            visited = [[False for _ in range(n)] for _ in range(n)]
            visited[y][x] = True
            
            while stack:
                cy, cx, path = stack.pop(0)
                if (cy, cx) == store[i]:
                    break
                    
                for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    ny, nx = cy+dy, cx+dx
                    if 0<=ny<n and 0<=nx<n and not visited[ny][nx] and grid[ny][nx] != 10:
                        np = path[:]
                        np.append((ny, nx))
                        stack.append((ny, nx, np))
                        visited[ny][nx] = True
                 

            tmp[i] = path[0]
    
    for i in range(1, m+1):
        if len(tmp[i])!=0:
            people[i] = tmp[i]
            if tmp[i] == store[i]:
                arival[i] = 1
                grid[people[i][0]][people[i][1]] = 10
                
    
    return

def deploy(time):
    for i in range(1, m+1):
        if i <= time and arival[i] == 0 and len(people[i]) == 0:
            y, x = store[i]
            stack = [(y, x, 0)]
            
            visited = [[False for _ in range(n)] for _ in range(n)]
            visited[y][x] = True
            
            base = []
            mv = n*2
            
            while stack:
                cy, cx, cnt = stack.pop(0)
                if cnt > mv:
                    continue
                if grid[cy][cx] == 1:
                    if cnt < mv:
                        mv = cnt
                        base = [(cy, cx)]
                    elif cnt==mv:
                        base.append((cy, cx))
                    continue
                    
                for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    ny, nx = cy+dy, cx+dx
                    if 0<=ny<n and 0<=nx<n and not visited[ny][nx] and grid[ny][nx] != 10:
                        stack.append((ny, nx, cnt+1))
                        visited[ny][nx] = True
                        
            base.sort()
            people[i] = base[0]
            grid[base[0][0]][base[0][1]] = 10
            
    return
                        
                    
                

n, m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

store = [(-1, -1)]
for id in range(1, m+1):
    y, x = map(int, input().split())
    store.append((y-1, x-1))
    grid[y-1][x-1] = -id

arival = [0 for _ in range(m+1)]
arival[0] = 1
debug = [[0 for _ in range(n)] for _ in range(n)]
people = [() for _ in range(m+1)]

time = 0
while True:
    time += 1
    move()
    if sum(arival) == m+1:
        print(time)
        break
    deploy(time)
    
# 중간에 못가는 부분이 생길 수 있어서 배정할때 저장한 경로 사용할 수 없음 (매번 bfs 돌려야함)