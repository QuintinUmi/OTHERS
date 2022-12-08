
map = [-1]
mapLoc = []
fixList = []

unproccessMap = [-1,    [-1, 14, 7, 3, 6],
                        [-1, 10, 1, 15, 11],
                        [-1, 12, 4, 2, 5],
                        [-1, 8, 9, 13, 0]]

# unproccessMap = [-1,    [-1, 7, 8, 22, 4, 5, 27],
#                         [-1, 19, 17, 18, 10, 1, 12],
#                         [-1, 13, 26, 6, 30, 20, 33],
#                         [-1, 31, 24, 3, 23, 15, 21],
#                         [-1, 25, 14, 34, 28, 29, 16],
#                         [-1, 2, 32, 9, 35, 11, 0]]

x_max, y_max = len(unproccessMap) - 1, len(unproccessMap[1]) - 1

dire = [-1, [-1, 0],
            [1, 0],
            [0, -1],
            [0, 1]]



class MapPoint:

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

def map_init(x, y, oriMap):

    for i in range(x * y):
        mapLoc.append([0, 0])
        fixList.append(False)
    for i in range(1, x + 1):
        temp = [-1]
        for j in range(1, y + 1):         
            temp.append(MapPoint(i, j, oriMap[i][j]))
            mapLoc[oriMap[i][j]] = [i, j]
        map.append(temp)

def edge_judgement(xi, yi, xf, yf, x, y):
    if(xi <= x <= xf and yi <= y <= yf):
        return True
    else:
        return False

def dire_sel(mPoint, xtarPoint, ytarPoint):

    if(xtarPoint < mPoint.x and ytarPoint < mPoint.y):
        return [dire[1], dire[3], [0, 0], dire[4]]
    if(xtarPoint > mPoint.x and ytarPoint > mPoint.y):
        return [dire[2], dire[4], [0, 0], dire[3]]
    if(xtarPoint > mPoint.x and ytarPoint < mPoint.y):
        return [dire[2], dire[3], [0, 0], dire[4]]
    if(xtarPoint < mPoint.x and ytarPoint > mPoint.y):
        return [dire[1], dire[4], [0, 0], dire[3]]

    if(xtarPoint == mPoint.x and ytarPoint < mPoint.y):
        return [dire[1], dire[2], dire[3], dire[4]]
    if(xtarPoint == mPoint.x and ytarPoint > mPoint.y):
        return [dire[1], dire[2], dire[4], dire[3]]
    if(xtarPoint > mPoint.x and ytarPoint == mPoint.y):
        return [dire[3], dire[4], dire[2], dire[1]]
    if(xtarPoint < mPoint.x and ytarPoint == mPoint.y):
        return [dire[3], dire[4], dire[1], dire[2]]

def swap(mPoint1, mPoint2):
    x1, y1 = mapLoc[mPoint1.num][0], mapLoc[mPoint1.num][1]
    x2, y2 = mapLoc[mPoint2.num][0], mapLoc[mPoint2.num][1]

    map[x1][y1].x, map[x1][y1].y = x2, y2
    map[x2][y2].x, map[x2][y2].y = x1, y1
    map[x1][y1], map[x2][y2] = map[x2][y2], map[x1][y1]
    mapLoc[mPoint1.num], mapLoc[mPoint2.num] = mapLoc[mPoint2.num], mapLoc[mPoint1.num]
    print_test()
    a = 0

def movement_2p(xi, yi, xf, yf, mPoint1, mPoint2, xtarPoint, ytarPoint):
    
    dis = 1
    xt, yt = mPoint1.x, mPoint1.y
    count = 2
    fixList[mPoint1.num], fixList[mPoint2.num] = True, True
    while(mPoint1.x != xtarPoint or mPoint1.y != ytarPoint):
        if(xf - xi + 1 > 2):
            if(count == 2):
                xt -= 1
                count -= 1
            elif(count == 1):
                yt -= 1
                count -= 1
        if(yf - yi + 1 > 2):
            if(count == 2):
                yt -= 1
                count -= 1
            elif(count == 1):
                xt -= 1
                count -= 1

        x, y = mPoint1.x, mPoint1.y
        dis = movement(xi, yi, xf, yf, mPoint1, xt, yt)
        tempPoint = map[x][y]
        movement(xi, yi, xf, yf, mPoint2, tempPoint.x, tempPoint.y)

    return 0

def movement(xi, yi, xf, yf, mPoint, xtarPoint, ytarPoint):
    
    # print_test()
    if(xtarPoint == mPoint.x and ytarPoint == mPoint.y):
        return 0

    d = dire_sel(mPoint, xtarPoint, ytarPoint)
    fixList[mPoint.num] = True

    if(mPoint.x + d[2][0] == mapLoc[0][0] and mPoint.y + d[2][1] == mapLoc[0][1]):
        fixList[mPoint.num] = False
        swap(map[mPoint.x][mPoint.y], map[mapLoc[0][0]][mapLoc[0][1]])
        return 0

    max_num = 0
    t_dire = -1
    for i in range(0, 3):
        if(not(xi <= mPoint.x + d[i][0] <= xf and yi <= mPoint.y + d[i][1] <= yf)):
            continue
        if(fixList[map[mPoint.x + d[i][0]][mPoint.y + d[i][1]].num]):
            continue
        if(mPoint.x + d[i][0] == xtarPoint and mPoint.y + d[i][1] == ytarPoint):
            max_num = map[mPoint.x + d[i][0]][mPoint.y + d[i][1]].num
            break
        max_num = max(max_num, map[mPoint.x + d[i][0]][mPoint.y + d[i][1]].num)

    if(max_num == 0):
        if(not(xi <= mPoint.x + d[3][0] <= xf and yi <= mPoint.y + d[3][1] <= yf)):
            pass
        elif(fixList[map[mPoint.x + d[3][0]][mPoint.y + d[3][1]].num]):
            pass
        else:
            max_num = max(max_num, map[mPoint.x + d[3][0]][mPoint.y + d[3][1]].num)
        if(max_num == 0):
            return -1
    nextPoint = map[mapLoc[max_num][0]][mapLoc[max_num][1]]

    xtarPoint = mapLoc[0][0]
    ytarPoint = mapLoc[0][1]

    if(xf - xi + 1 <= 2 and yf - yi + 1 <= 2 and mPoint.num == xi * yf and nextPoint.x == xi and nextPoint.y == yf):
        return -1
        

    if(xf - xi + 1 > 2):
        if(nextPoint.x == xi and nextPoint.y == yf and mPoint.num == (nextPoint.x - 1) * yf + nextPoint.y 
            and fixList[map[nextPoint.x][nextPoint.y - 1].num] == False):
            dis = 1
            while(dis):
                dis = movement(xi, yf - 1, xi + 2, yf, mPoint, xi + 2, yf)
                if(dis == -1):
                    return -1
            fixList[mPoint.num] = True

            dis = 1
            tempPoint = map[xi][yf - 1]
            while(dis):
                dis = movement(xi, yf - 1, xi + 2, yf, tempPoint, xi + 1, yf)
                if(dis == -1):
                    return -1
            fixList[tempPoint.num] = True      

            movement_2p(xi, yf - 1, xi + 2, yf, tempPoint, mPoint, xi, yf - 1)

            fixList[tempPoint.num] = False

            return 0
        else:
            movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)
            fixList[mPoint.num] = False
            nextPoint = map[mapLoc[0][0]][mapLoc[0][1]]
            swap(mPoint, nextPoint)
            return 1
    else:
        if(nextPoint.x == xf and nextPoint.y == yi and mPoint.num == (nextPoint.x - 1) * y_max + nextPoint.y):
            dis = 1
            while(dis):
                dis = movement(xi, yi, xi + 1, yi + 2, mPoint, xf, yf)
                if(dis == -1):
                    return -1
            fixList[mPoint.num] = True

            dis = 1
            tempPoint = map[xi][yi]
            while(dis):
                dis = movement(xi, yi, xi + 1, yi + 2, tempPoint, xf, yf - 1)
                if(dis == -1):
                    return -1    
            fixList[tempPoint.num] = True

            movement_2p(xi, yi, xi + 1, yi + 2, tempPoint, mPoint, xi, yi)

            fixList[tempPoint.num] = False

            return 0
        else:
            movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)
            fixList[mPoint.num] = False
            nextPoint = map[mapLoc[0][0]][mapLoc[0][1]]
            swap(mPoint, nextPoint)
            return 1


def map_solve(x, y):
       
    for num in range(1, (x - 1)* y + 1):

        # print_test()
        if(num <= (x - 2) * y):
            dis = 1
            while(dis):

                dis = movement((num - 1) // y + 1, 1, x, y, 
                                map[mapLoc[num][0]][mapLoc[num][1]], 
                                (num - 1) // y + 1, (num - 1) % y + 1)
                if(dis == -1):
                    break
            fixList[num] = True
            continue

        if((x - 2) * y < num <= (x - 2) * y + y - 2 and dis != -1):
            if(num <= (x - 1) * y):
                dis = 1
                while(dis):
                    dis = movement(x - 1, num - (x - 2) * y, x, y, 
                                    map[mapLoc[num][0]][mapLoc[num][1]], 
                                    (num - 1) // y + 1, (num - 1) % y + 1)
                fixList[num] = True    
                dis = 1
                while(dis):
                    dis = movement(x - 1, num - (x - 2) * y, x, y, 
                                    map[mapLoc[num + y][0]][mapLoc[num + y][1]], 
                                    (num + y - 1) // y + 1, (num + y - 1) % y + 1)        
                fixList[num + y] = True
            continue

        if((x - 2) * y + y - 2 < num and dis != -1):
            dis = 1
            while(dis):
                dis = movement(x - 1, num - (x - 1) * y, x, y, 
                                    map[mapLoc[0][0]][mapLoc[0][1]], 
                                    x_max, y_max)
                if(dis == -1):
                    break
            
            fixList[num] = True
            continue

    if(check_res()):
        return 0
    else:
        return -1
        
        
    return dis
            

def check_res():
    for i in range(1, x_max * y_max):
        if((mapLoc[i][0] - 1) * y_max + mapLoc[i][1] != i):
            return False

    return True

def print_test():

    print()
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            # print(map[i][j].num, (map[i][j].x, map[i][j].y), end=' ')
            print(map[i][j].num, end=' ')
        print()
    
    

def main():

    x_max, y_max = len(unproccessMap) - 1, len(unproccessMap[1]) - 1
    map_init(x_max, y_max, unproccessMap)
    res = map_solve(x_max, y_max)
    
    print(res)
    print()
    print_test()


if __name__ == "__main__":
    main()