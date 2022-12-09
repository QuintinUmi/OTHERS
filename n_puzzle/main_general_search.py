import pdb
import time
import pickle
import map_generator

time_start=time.time()

pz_map = [-1]
mapLoc = []
fixList = []

PROCEDURE_STORAGE = []
DEEP = 0
MAX_DEEP = 0

# unproccessMap = [-1,    [-1, 14, 7, 3, 6],
#                         [-1, 10, 1, 15, 11],
#                         [-1, 12, 4, 2, 5],
#                         [-1, 8, 9, 13, 0]]

# unproccessMap = [-1,    [-1, 20, 18, 3, 10, 19],
#                         [-1, 24, 1, 14, 5, 23],
#                         [-1, 2, 9, 13, 21, 6],
#                         [-1, 22, 11, 7, 12, 8],
#                         [-1, 16, 17, 4, 15, 0]]

# unproccessMap = [-1,    [-1, 7, 8, 22, 4, 5, 27],
#                         [-1, 19, 17, 18, 10, 1, 12],
#                         [-1, 13, 26, 6, 30, 20, 33],
#                         [-1, 31, 24, 3, 23, 15, 21],
#                         [-1, 25, 14, 34, 28, 29, 16],
#                         [-1, 2, 32, 9, 35, 11, 0]]

unproccessMap = [-1,    [-1, 20, 63, 12, 4, 11, 6, 52, 32],      
                        [-1, 9, 38, 13, 3, 56, 62, 49, 16],
                        [-1, 15, 18, 23, 44, 26, 36, 19, 31],
                        [-1, 29, 17, 27, 28, 25, 30, 43, 51],
                        [-1, 33, 14, 35, 7, 37, 45, 39, 40],
                        [-1, 41, 42, 24, 57, 8, 46, 47, 48],
                        [-1, 55, 34, 5, 22, 53, 50, 54, 10],
                        [-1, 21, 58, 59, 60, 61, 1, 2, 0]]

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
        pz_map.append(temp)

    PROCEDURE_STORAGE.append(pickle.loads(pickle.dumps(pz_map)))

def edge_judgement(xi, yi, xf, yf, x, y):
    if(xi <= x <= xf and yi <= y <= yf):
        return True
    else:
        return False

def dire_sel(curPoint, xtarPoint, ytarPoint):

    if(xtarPoint < curPoint.x and ytarPoint < curPoint.y):
        return [dire[1], dire[3], dire[2], dire[4]]
    if(xtarPoint > curPoint.x and ytarPoint > curPoint.y):
        return [dire[2], dire[4], dire[1], dire[3]]
    if(xtarPoint > curPoint.x and ytarPoint < curPoint.y):
        return [dire[2], dire[3], dire[1], dire[4]]
    if(xtarPoint < curPoint.x and ytarPoint > curPoint.y):
        return [dire[1], dire[4], dire[2], dire[3]]

    if(xtarPoint == curPoint.x and ytarPoint < curPoint.y):
        return [dire[3], dire[1], dire[2], dire[4]]
    if(xtarPoint == curPoint.x and ytarPoint > curPoint.y):
        return [dire[4], dire[1], dire[2], dire[3]]
    if(xtarPoint > curPoint.x and ytarPoint == curPoint.y):
        return [dire[2], dire[3], dire[4], dire[1]]
    if(xtarPoint < curPoint.x and ytarPoint == curPoint.y):
        return [dire[1], dire[3], dire[4], dire[2]]

def swap(curPoint1, curPoint2):
    x1, y1 = mapLoc[curPoint1.num][0], mapLoc[curPoint1.num][1]
    x2, y2 = mapLoc[curPoint2.num][0], mapLoc[curPoint2.num][1]

    pz_map[x1][y1].x, pz_map[x1][y1].y = x2, y2
    pz_map[x2][y2].x, pz_map[x2][y2].y = x1, y1
    pz_map[x1][y1], pz_map[x2][y2] = pz_map[x2][y2], pz_map[x1][y1]
    mapLoc[curPoint1.num], mapLoc[curPoint2.num] = mapLoc[curPoint2.num], mapLoc[curPoint1.num]
    PROCEDURE_STORAGE.append(pickle.loads(pickle.dumps(pz_map)))
    # print_test()
    a = 0

def movement_2p(xi, yi, xf, yf, curPoint1, curPoint2, xtarPoint, ytarPoint):
    global DEEP 
    dis = 1
    xt, yt = curPoint1.x, curPoint1.y
    count = 2
    fixList[curPoint1.num] = True
    fixList[curPoint2.num] = True
    while(curPoint1.x != xtarPoint or curPoint1.y != ytarPoint):
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

        x, y = curPoint1.x, curPoint1.y
        DEEP += 1
        dis = movement(xi, yi, xf, yf, curPoint1, xt, yt)
        DEEP -= 1
        tempPoint = pz_map[x][y]
        DEEP += 1
        movement(xi, yi, xf, yf, curPoint2, tempPoint.x, tempPoint.y)
        DEEP -= 1
        fixList[curPoint1.num] = True
        fixList[curPoint2.num] = True

    return 0

def movement(xi, yi, xf, yf, curPoint, xtarPoint, ytarPoint):
    global DEEP, MAX_DEEP
    MAX_DEEP = max(MAX_DEEP, DEEP)
    # print("------------------------------------------------ Recursion depth: ", DEEP)
    if(DEEP > 10):
        a = 0
    # print_test()
    if(xtarPoint == curPoint.x and ytarPoint == curPoint.y):
        return 0

    d = dire_sel(curPoint, xtarPoint, ytarPoint)
    fixList[curPoint.num] = True

    if(curPoint.x + d[0][0] == mapLoc[0][0] and curPoint.y + d[0][1] == mapLoc[0][1]
        and mapLoc[0][0] == xtarPoint and mapLoc[0][1] == ytarPoint):
        fixList[curPoint.num] = False
        swap(pz_map[curPoint.x][curPoint.y], pz_map[mapLoc[0][0]][mapLoc[0][1]])
        return 0

    dire_stack = []
    num = 0
    for i in range(0, 3):
        if(not(xi <= curPoint.x + d[i][0] <= xf and yi <= curPoint.y + d[i][1] <= yf)):
            continue
        if(fixList[pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num]):
            continue
        if(curPoint.x + d[i][0] == xtarPoint and curPoint.y + d[i][1] == ytarPoint):
            num = pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num
            break

        dire_stack.append(pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num)

    if(num != 0):
        dire_stack = [pz_map[mapLoc[num][0]][mapLoc[num][1]].num] + dire_stack
    if(xi <= curPoint.x + d[3][0] <= xf and yi <= curPoint.y + d[3][1] <= yf 
        and not fixList[pz_map[curPoint.x + d[3][0]][curPoint.y + d[3][1]].num]):
        dire_stack.append(pz_map[curPoint.x + d[3][0]][curPoint.y + d[3][1]].num)
    if(len(dire_stack) == 0):
        fixList[curPoint.num] = False
        return -1

    for i in range(len(dire_stack)):

        nextPoint = pz_map[mapLoc[dire_stack[i]][0]][mapLoc[dire_stack[i]][1]]

        xtarPoint = mapLoc[0][0]
        ytarPoint = mapLoc[0][1]

        # if(xf - xi + 1 <= 2 and yf - yi + 1 <= 2 and curPoint.num == xi * yf and nextPoint.x == xi and nextPoint.y == yf):
        #     continue
        if(DEEP > 10):
            a = 0    

        if(xf - xi + 1 > 2):
            if(nextPoint.x == xi and nextPoint.y == yf and curPoint.num == (nextPoint.x - 1) * y_max + nextPoint.y 
                and fixList[pz_map[nextPoint.x][nextPoint.y - 1].num] == True
                and curPoint.x - 1 == xi and curPoint.y == yf):
                dis = 1
                while(dis):
                    DEEP += 1
                    dis = movement(xi, yf - 1, xi + 2, yf, curPoint, xi + 2, yf)
                    DEEP -= 1
                    if(dis == -1):
                        return -1
                fixList[curPoint.num] = True

                dis = 1
                tempPoint = pz_map[xi][yf - 1]
                while(dis):
                    DEEP += 1
                    dis = movement(xi, yf - 1, xi + 2, yf, tempPoint, xi + 1, yf)
                    DEEP -= 1
                    if(dis == -1):
                        return -1
                fixList[tempPoint.num] = True      
                DEEP += 1
                movement_2p(xi, yf - 1, xi + 2, yf, tempPoint, curPoint, xi, yf - 1)
                DEEP -= 1

                return 0
            else:
                dis = 1
                DEEP += 1
                dis = movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)   
                DEEP -= 1           
                if(dis == -1):
                    fixList[nextPoint.num] = False
                    continue
                fixList[curPoint.num] = False
                nextPoint = pz_map[mapLoc[0][0]][mapLoc[0][1]]
                swap(curPoint, nextPoint)
                return 1
        else:
            if(nextPoint.x == xf and nextPoint.y == yi and curPoint.num == (nextPoint.x - 1) * y_max + nextPoint.y
                and curPoint.x == xi + 1 and curPoint.y == yi + 1):
                dis = 1
                while(dis):
                    DEEP += 1
                    dis = movement(xi, yi, xi + 1, yf, curPoint, xf, yi + 2)
                    DEEP -= 1
                    if(dis == -1):
                        return -1
                fixList[curPoint.num] = True

                dis = 1
                tempPoint = pz_map[xi][yi]
                while(dis):
                    fixList[curPoint.num] = True
                    DEEP += 1
                    dis = movement(xi, yi, xi + 1, yf, tempPoint, xf, yi + 1)
                    DEEP -= 1
                    if(dis == -1):
                        return -1   
                fixList[tempPoint.num] = True
                DEEP += 1
                movement_2p(xi, yi, xi + 1, yi + 2, tempPoint, curPoint, xi, yi)
                DEEP -= 1

                return 0
            else:
                dis = 1
                DEEP += 1
                dis = movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)
                DEEP -= 1
                if(dis == -1):
                    fixList[nextPoint.num] = False
                    continue
                fixList[curPoint.num] = False
                nextPoint = pz_map[mapLoc[0][0]][mapLoc[0][1]]
                swap(curPoint, nextPoint)
                return 1

    return -1


def map_solve(x, y):
    global DEEP   
    print_test()

    for num in range(1, (x - 1)* y + 1):

        # print_test()
        if(num <= (x - 2) * y):
            dis = 1
            while(dis):
                DEEP += 1
                if(num == 19):
                    a=0
                dis = movement((num - 1) // y + 1, 1, x, y, 
                                pz_map[mapLoc[num][0]][mapLoc[num][1]], 
                                (num - 1) // y + 1, (num - 1) % y + 1)
                DEEP -= 1
                if(dis == -1):
                    return -1
            fixList[num] = True
            continue

        if((x - 2) * y < num <= (x - 2) * y + y - 2 and dis != -1):
            if(num <= (x - 1) * y):
                dis = 1
                while(dis):
                    DEEP += 1
                    dis = movement(x - 1, num - (x - 2) * y, x, y, 
                                    pz_map[mapLoc[num][0]][mapLoc[num][1]], 
                                    (num - 1) // y + 1, (num - 1) % y + 1)
                    DEEP -= 1
                fixList[num] = True    
                dis = 1
                while(dis):
                    DEEP += 1
                    dis = movement(x - 1, num - (x - 2) * y, x, y, 
                                    pz_map[mapLoc[num + y][0]][mapLoc[num + y][1]], 
                                    (num + y - 1) // y + 1, (num + y - 1) % y + 1)        
                    DEEP -= 1
                fixList[num + y] = True
            continue

        if((x - 2) * y + y - 2 < num and dis != -1):
            dis = 1
            while(dis):
                DEEP += 1
                dis = movement(x - 1, y - 1, x, y, 
                                    pz_map[mapLoc[num][0]][mapLoc[num][1]], 
                                    x - 1, y - 1)
                DEEP -= 1
                if(dis == -1):
                    return -1
            fixList[num] = True

            dis = 1
            while(dis):
                DEEP += 1
                dis = movement(x - 1, y - 1, x, y, 
                                    pz_map[mapLoc[num + y][0]][mapLoc[num + y][1]], 
                                    x, y - 1)
                DEEP -= 1
                if(dis == -1):
                    return -1
            fixList[num + y] = True

            dis = 1
            while(dis):
                DEEP += 1
                dis = movement(x - 1, y - 1, x, y, 
                                    pz_map[mapLoc[num + 1][0]][mapLoc[num + 1][1]], 
                                    x - 1, y)
                DEEP -= 1
                if(dis == -1):
                    return -1           
            fixList[num + 1] = True

            break

    if(check_res()):
        return 0
    else:
        return -1

            

def check_res():
    for i in range(1, x_max * y_max):
        if((mapLoc[i][0] - 1) * y_max + mapLoc[i][1] != i):
            return False

    return True

def print_test():

    print()
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
            print(pz_map[i][j].num, end=' ')
        print()

def print_map(p_map):

    print()
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
            print(p_map[i][j].num, end=' ')
        print()

def write_res(f, w_map):
    
    f.write("\n")
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
            f.write("{} ".format(w_map[i][j].num))
        f.write("\n")
    
    

def main():

    x_max, y_max = len(unproccessMap) - 1, len(unproccessMap[1]) - 1
    map_init(x_max, y_max, unproccessMap)
    res = map_solve(x_max, y_max)
    print()
    print("--------------------Result---------------------")
    print_test()
    print("-----------------------------------------------")
    print("Status (0->Success, -1->No Solution): ", res)
    print("Total Steps: ", len(PROCEDURE_STORAGE))
    print("Deepest recursion depth: ", MAX_DEEP)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')
    print()

    input("Press ENTER to show and write the procedure of the solution in a file where the upper level of this source code is  ")

    for w_map in PROCEDURE_STORAGE:
        print_map(w_map)

    input("\nPress ENTER to write in file... (Note: The program may not create the file if no Administrator Permissions) ")
    f = open(".\\result.txt", 'w')
    for w_map in PROCEDURE_STORAGE:
        write_res(f, w_map)
    print("", file=f)
    print("--------------------Result---------------------", file=f)
    write_res(f, pz_map)
    print("-----------------------------------------------", file=f)
    print("Status (0->Success, -1->No Solution): ", res, file=f)
    print("Total Steps: ", len(PROCEDURE_STORAGE), file=f)
    print("Deepest recursion depth: ", MAX_DEEP, file=f)
    f.close()

    input("\nPress ENTER to continue...  ")



if __name__ == "__main__":
    main()