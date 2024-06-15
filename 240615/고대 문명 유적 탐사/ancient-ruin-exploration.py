def recover():
    global result, A
    
    while True:
        for x in range(5):
            for y in range(4, -1, -1):
                if A[y][x] == 0:
                    rn = num.pop(0)
                    A[y][x] = rn
        value, A = find(A)
        if value==0:
            break
        else:
            result += value
        
    return        

def find(tmp_map):
    DY = [-1, 1, 0, 0]
    DX = [0, 0, -1, 1]
    
    value = 0
    visited = [[False for _ in range(5)] for _ in range(5)]
    
    for y in range(5):
        for x in range(5):
            if not visited[y][x]:
                visited[y][x] = True
                cnt = 1
                stack = [(y, x)]
                rm = [(y, x)]
                
                while stack:
                    ny, nx = stack.pop(0)
                    for i in range(4):
                        nny, nnx = ny+DY[i], nx+DX[i]
                        if 0<=nny<5 and 0<=nnx<5 and not visited[nny][nnx]:
                            if tmp_map[nny][nnx] == tmp_map[ny][nx]:
                                visited[nny][nnx] = True
                                cnt += 1
                                stack.append((nny, nnx))
                                rm.append((nny, nnx))
                                # stack에 직접 cnt를 넣으면 십자가 부분에서 카운트가 누락됌
                
                if cnt > 2:
                    value+=cnt
                    for ry, rx in rm:
                        tmp_map[ry][rx] = 0
                        
    return value, tmp_map
                    
def rotate(y, x, d):
    value = 0
    tmp = [row[:] for row in A] # 깊은 복사는 이렇게 해야한다. 2차원 배열에서 A[:] 이거는 얇은 복사, 그러나 1차원 배열에서 A[:]는 깊은 복사
    tmp_map = [row[:] for row in A]
    for _ in range(d):
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                oy, ox = i-(y-1), j-(x-1)
                ry, rx = ox, 3-oy-1
                tmp[ry+y-1][rx+x-1] = tmp_map[i][j]
                
        tmp_map = [row[:] for row in tmp]
        
    value, tmp_map = find(tmp_map)
    
    return value, tmp_map

def search():
    global result, A
    maxv = 0
    maxm = None
    
    for d in range(1, 4): # 제발 범위체크좀 확실히하자 (나중에 디버깅으로 찾으려면 너무 오래걸려 차라리 꼼꼼하게 좀 봐) (이걸 1, 3이라고 하니까 270도가 적용이 안되잖아) (그럼에도 디버깅으로 찾아야 한다면 예시에서 적용이 안된 조건 체크해보자; 이경우에는 270도를 돈적이 없으니 거기서 에러 발생했을 수 있다.)
        for x in range(1, 4):
            for y in range(1, 4):
                value, tmp_map = rotate(y, x, d)
                if maxv < value:
                    maxv = value
                    maxm = tmp_map
                    
    # 최대값 또는 최소값이 여러 개인 경우에 조건이 달린 것은 
    # 1) for문 배치를 통해 우선순위 높은 순서대로 돌리면서 최대값만 찾아주면됌
    # 2) list에 조건에 맞는 값들을 포함하여 중복되는 값들을 저장하고 sort를 사용하는 방식
    # 이 두 방법 중 2번이 가시적으로 보긴 좋으나 효율성이 안좋을 수 있음

    if maxv == 0:
        return False
    else:
        A = maxm
        result += maxv
        return True
    

K, M = map(int, input().split())
A = []
for _ in range(5):
    A.append(list(map(int, input().split())))
    
num = list(map(int, input().split()))

for _ in range(K):
    result = 0
    if not search():
        break
    recover()
    print(result, end=' ')