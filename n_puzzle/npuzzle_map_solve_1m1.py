import pickle
import time

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

# unproccessMap = [-1,    [-1, 20, 63, 12, 4, 11, 6, 52, 32],      
#                         [-1, 9, 38, 13, 3, 56, 62, 49, 16],
#                         [-1, 15, 18, 23, 44, 26, 36, 19, 31],
#                         [-1, 29, 17, 27, 28, 25, 30, 43, 51],
#                         [-1, 33, 14, 35, 7, 37, 45, 39, 40],
#                         [-1, 41, 42, 24, 57, 8, 46, 47, 48],
#                         [-1, 55, 34, 5, 22, 53, 50, 54, 10],
#                         [-1, 21, 58, 59, 60, 61, 1, 2, 0]]

class MapPoint:

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

class MapSolve:

    def __init__(self):
        self.pz_map = [-1]
        self.mapLoc = []
        self.fixList = []
        self.procedureStorage = []
        self.deep = 0
        self.max_deep = 0
        self.x_max, self.y_max = 0, 0

        self.dire = [-1, [-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1]]

    def map_init(self, x, y, oriMap):

        self.x_max, self.y_max = x, y
        for i in range(x * y):
            self.mapLoc.append([0, 0])
            self.fixList.append(False)
        for i in range(1, x + 1):
            temp = [-1]
            for j in range(1, y + 1):         
                temp.append(MapPoint(i, j, oriMap[i][j]))
                self.mapLoc[oriMap[i][j]] = [i, j]
            self.pz_map.append(temp)

        self.procedureStorage.append(pickle.loads(pickle.dumps(self.pz_map)))

    def edge_judgement(xi, yi, xf, yf, x, y):
        if(xi <= x <= xf and yi <= y <= yf):
            return True
        else:
            return False

    def dire_sel(self, curPoint, xtarPoint, ytarPoint):

        if(xtarPoint < curPoint.x and ytarPoint < curPoint.y):
            return [self.dire[1], self.dire[3], self.dire[2], self.dire[4]]
        if(xtarPoint > curPoint.x and ytarPoint > curPoint.y):
            return [self.dire[2], self.dire[4], self.dire[1], self.dire[3]]
        if(xtarPoint > curPoint.x and ytarPoint < curPoint.y):
            return [self.dire[2], self.dire[3], self.dire[1], self.dire[4]]
        if(xtarPoint < curPoint.x and ytarPoint > curPoint.y):
            return [self.dire[1], self.dire[4], self.dire[2], self.dire[3]]

        if(xtarPoint == curPoint.x and ytarPoint < curPoint.y):
            return [self.dire[3], self.dire[1], self.dire[2], self.dire[4]]
        if(xtarPoint == curPoint.x and ytarPoint > curPoint.y):
            return [self.dire[4], self.dire[1], self.dire[2], self.dire[3]]
        if(xtarPoint > curPoint.x and ytarPoint == curPoint.y):
            return [self.dire[2], self.dire[3], self.dire[4], self.dire[1]]
        if(xtarPoint < curPoint.x and ytarPoint == curPoint.y):
            return [self.dire[1], self.dire[3], self.dire[4], self.dire[2]]

    def swap(self, curPoint1, curPoint2):
        x1, y1 = self.mapLoc[curPoint1.num][0], self.mapLoc[curPoint1.num][1]
        x2, y2 = self.mapLoc[curPoint2.num][0], self.mapLoc[curPoint2.num][1]

        self.pz_map[x1][y1].x, self.pz_map[x1][y1].y = x2, y2
        self.pz_map[x2][y2].x, self.pz_map[x2][y2].y = x1, y1
        self.pz_map[x1][y1], self.pz_map[x2][y2] = self.pz_map[x2][y2], self.pz_map[x1][y1]
        self.mapLoc[curPoint1.num], self.mapLoc[curPoint2.num] = self.mapLoc[curPoint2.num], self.mapLoc[curPoint1.num]
        self.procedureStorage.append(pickle.loads(pickle.dumps(self.pz_map)))
        # print_test()
        a = 0

    def movement_2p(self, xi, yi, xf, yf, curPoint1, curPoint2, xtarPoint, ytarPoint):
        dis = 1
        xt, yt = curPoint1.x, curPoint1.y
        count = 2
        self.fixList[curPoint1.num] = True
        self.fixList[curPoint2.num] = True
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
            self.deep += 1
            dis = self.movement(xi, yi, xf, yf, curPoint1, xt, yt)
            self.deep -= 1
            tempPoint = self.pz_map[x][y]
            self.deep += 1
            self.movement(xi, yi, xf, yf, curPoint2, tempPoint.x, tempPoint.y)
            self.deep -= 1
            self.fixList[curPoint1.num] = True
            self.fixList[curPoint2.num] = True

        return 0

    def movement(self, xi, yi, xf, yf, curPoint, xtarPoint, ytarPoint):

        self.max_deep = max(self.max_deep, self.deep)
        # print("------------------------------------------------ Recursion depth: ", self.deep)
        if(self.deep > 10):
            a = 0
        # print_test()
        if(xtarPoint == curPoint.x and ytarPoint == curPoint.y):
            return 0

        d = self.dire_sel(curPoint, xtarPoint, ytarPoint)
        self.fixList[curPoint.num] = True

        if(curPoint.x + d[0][0] == self.mapLoc[0][0] and curPoint.y + d[0][1] == self.mapLoc[0][1]
            and self.mapLoc[0][0] == xtarPoint and self.mapLoc[0][1] == ytarPoint):
            self.fixList[curPoint.num] = False
            self.swap(self.pz_map[curPoint.x][curPoint.y], self.pz_map[self.mapLoc[0][0]][self.mapLoc[0][1]])
            return 0

        dire_stack = []
        num = 0
        for i in range(0, 3):
            if(not(xi <= curPoint.x + d[i][0] <= xf and yi <= curPoint.y + d[i][1] <= yf)):
                continue
            if(self.fixList[self.pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num]):
                continue
            if(curPoint.x + d[i][0] == xtarPoint and curPoint.y + d[i][1] == ytarPoint):
                num = self.pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num
                break

            dire_stack.append(self.pz_map[curPoint.x + d[i][0]][curPoint.y + d[i][1]].num)

        if(num != 0):
            dire_stack = [self.pz_map[self.mapLoc[num][0]][self.mapLoc[num][1]].num] + dire_stack
        if(xi <= curPoint.x + d[3][0] <= xf and yi <= curPoint.y + d[3][1] <= yf 
            and not self.fixList[self.pz_map[curPoint.x + d[3][0]][curPoint.y + d[3][1]].num]):
            dire_stack.append(self.pz_map[curPoint.x + d[3][0]][curPoint.y + d[3][1]].num)
        if(len(dire_stack) == 0):
            self.fixList[curPoint.num] = False
            return -1

        for i in range(len(dire_stack)):

            nextPoint = self.pz_map[self.mapLoc[dire_stack[i]][0]][self.mapLoc[dire_stack[i]][1]]

            xtarPoint = self.mapLoc[0][0]
            ytarPoint = self.mapLoc[0][1]

            # if(xf - xi + 1 <= 2 and yf - yi + 1 <= 2 and curPoint.num == xi * yf and nextPoint.x == xi and nextPoint.y == yf):
            #     continue
            if(self.deep > 10):
                a = 0    

            if(xf - xi + 1 > 2):
                if(nextPoint.x == xi and nextPoint.y == yf and curPoint.num == (nextPoint.x - 1) * self.y_max + nextPoint.y 
                    and self.fixList[self.pz_map[nextPoint.x][nextPoint.y - 1].num] == True
                    and curPoint.x - 1 == xi and curPoint.y == yf):
                    dis = 1
                    while(dis):
                        self.deep += 1
                        dis = self.movement(xi, yf - 1, xi + 2, yf, curPoint, xi + 2, yf)
                        self.deep -= 1
                        if(dis == -1):
                            return -1
                    self.fixList[curPoint.num] = True

                    dis = 1
                    tempPoint = self.pz_map[xi][yf - 1]
                    while(dis):
                        self.deep += 1
                        dis = self.movement(xi, yf - 1, xi + 2, yf, tempPoint, xi + 1, yf)
                        self.deep -= 1
                        if(dis == -1):
                            return -1
                    self.fixList[tempPoint.num] = True      
                    self.deep += 1
                    self.movement_2p(xi, yf - 1, xi + 2, yf, tempPoint, curPoint, xi, yf - 1)
                    self.deep -= 1

                    return 0
                else:
                    dis = 1
                    self.deep += 1
                    dis = self.movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)   
                    self.deep -= 1           
                    if(dis == -1):
                        self.fixList[nextPoint.num] = False
                        continue
                    self.fixList[curPoint.num] = False
                    nextPoint = self.pz_map[self.mapLoc[0][0]][self.mapLoc[0][1]]
                    self.swap(curPoint, nextPoint)
                    return 1
            elif(yf - yi + 1 > 2):
                if(nextPoint.x == xf and nextPoint.y == yi and curPoint.num == (nextPoint.x - 1) * self.y_max + nextPoint.y
                    and curPoint.x == xi + 1 and curPoint.y == yi + 1):
                    dis = 1
                    while(dis):
                        self.deep += 1
                        dis = self.movement(xi, yi, xi + 1, yf, curPoint, xf, yi + 2)
                        self.deep -= 1
                        if(dis == -1):
                            return -1
                    self.fixList[curPoint.num] = True

                    dis = 1
                    tempPoint = self.pz_map[xi][yi]
                    while(dis):
                        self.fixList[curPoint.num] = True
                        self.deep += 1
                        dis = self.movement(xi, yi, xi + 1, yf, tempPoint, xf, yi + 1)
                        self.deep -= 1
                        if(dis == -1):
                            return -1   
                    self.fixList[tempPoint.num] = True
                    self.deep += 1
                    self.movement_2p(xi, yi, xi + 1, yi + 2, tempPoint, curPoint, xi, yi)
                    self.deep -= 1

                    return 0
                else:
                    dis = 1
                    self.deep += 1
                    dis = self.movement(xi, yi, xf, yf, nextPoint, xtarPoint, ytarPoint)
                    self.deep -= 1
                    if(dis == -1):
                        self.fixList[nextPoint.num] = False
                        continue
                    self.fixList[curPoint.num] = False
                    nextPoint = self.pz_map[self.mapLoc[0][0]][self.mapLoc[0][1]]
                    self.swap(curPoint, nextPoint)
                    return 1

        return -1


    def map_solve(self, x, y):
        # print_test()

        for num in range(1, (x - 1)* y + 1):

            # print_test()
            if(num <= (x - 2) * y):
                dis = 1
                while(dis):
                    self.deep += 1
                    if(num == 19):
                        a=0
                    dis = self.movement((num - 1) // y + 1, 1, x, y, 
                                    self.pz_map[self.mapLoc[num][0]][self.mapLoc[num][1]], 
                                    (num - 1) // y + 1, (num - 1) % y + 1)
                    self.deep -= 1
                    if(dis == -1):
                        return -1
                self.fixList[num] = True
                continue

            if((x - 2) * y < num <= (x - 2) * y + y - 2 and dis != -1):
                if(num <= (x - 1) * y):
                    dis = 1
                    while(dis):
                        self.deep += 1
                        dis = self.movement(x - 1, num - (x - 2) * y, x, y, 
                                        self.pz_map[self.mapLoc[num][0]][self.mapLoc[num][1]], 
                                        (num - 1) // y + 1, (num - 1) % y + 1)
                        self.deep -= 1
                    self.fixList[num] = True    
                    dis = 1
                    while(dis):
                        self.deep += 1
                        dis = self.movement(x - 1, num - (x - 2) * y, x, y, 
                                        self.pz_map[self.mapLoc[num + y][0]][self.mapLoc[num + y][1]], 
                                        (num + y - 1) // y + 1, (num + y - 1) % y + 1)        
                        self.deep -= 1
                    self.fixList[num + y] = True
                continue

            if((x - 2) * y + y - 2 < num and dis != -1):
                dis = 1
                while(dis):
                    self.deep += 1
                    dis = self.movement(x - 1, y - 1, x, y, 
                                        self.pz_map[self.mapLoc[num][0]][self.mapLoc[num][1]], 
                                        x - 1, y - 1)
                    self.deep -= 1
                    if(dis == -1):
                        return -1
                self.fixList[num] = True

                dis = 1
                while(dis):
                    self.deep += 1
                    dis = self.movement(x - 1, y - 1, x, y, 
                                        self.pz_map[self.mapLoc[num + y][0]][self.mapLoc[num + y][1]], 
                                        x, y - 1)
                    self.deep -= 1
                    if(dis == -1):
                        return -1
                self.fixList[num + y] = True

                dis = 1
                while(dis):
                    self.deep += 1
                    dis = self.movement(x - 1, y - 1, x, y, 
                                        self.pz_map[self.mapLoc[num + 1][0]][self.mapLoc[num + 1][1]], 
                                        x - 1, y)
                    self.deep -= 1
                    if(dis == -1):
                        return -1           
                self.fixList[num + 1] = True

                break

        if(self.check_res()):
            return 0
        else:
            return -1

    def check_res(self):
        for i in range(1, self.x_max * self.y_max):
            if((self.mapLoc[i][0] - 1) * self.y_max + self.mapLoc[i][1] != i):
                return False

        return True

    
    def procedure(self):
        return self.procedureStorage

    def print_test(self):

        print()
        for i in range(1, self.x_max + 1):
            for j in range(1, self.y_max + 1):
                # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
                print("{:^6d}".format(self.pz_map[i][j].num), end=' ')
            print()

    def print_map(self, p_map):

        print()
        for i in range(1, self.x_max + 1):
            for j in range(1, self.y_max + 1):
                # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
                print("{:^6d}".format(p_map[i][j].num), end=' ')
            print()

    def write_res(self, f, w_map):
        
        f.write("\n")
        for i in range(1, self.x_max + 1):
            for j in range(1, self.y_max + 1):
                # print(pz_map[i][j].num, (pz_map[i][j].x, pz_map[i][j].y), end=' ')
                print("{:^6d}".format(w_map[i][j].num), file=f)
            f.write("\n")

if __name__ == "__main__":
    
    unproccessMap = [-1,    [-1, 20, 63, 12, 4, 11, 6, 52, 32],      
                            [-1, 9, 38, 13, 3, 56, 62, 49, 16],
                            [-1, 15, 18, 23, 44, 26, 36, 19, 31],
                            [-1, 29, 17, 27, 28, 25, 30, 43, 51],
                            [-1, 33, 14, 35, 7, 37, 45, 39, 40],
                            [-1, 41, 42, 24, 57, 8, 46, 47, 48],
                            [-1, 55, 34, 5, 22, 53, 50, 54, 10],
                            [-1, 21, 58, 59, 60, 61, 1, 2, 0]]

    x_max, y_max = len(unproccessMap) - 1, len(unproccessMap[1]) - 1
    time_start = time.time()
    np = MapSolve()
    np.map_init(x_max, y_max, unproccessMap)
    print("\nProccessing...\n")
    res = np.map_solve(x_max, y_max)
    time_end = time.time()
    print()
    print("--------------------Result---------------------")
    np.print_test()
    print("-----------------------------------------------")
    print("Status (0->Success, -1->No Solution): ", res)
    print("Total Steps: ", len(np.procedureStorage))
    print("Deepest recursion depth: ", np.max_deep)
    print('time cost',time_end - time_start,'s')
    print()

    input("Press ENTER to show the procedure of the solution in a file where the upper level of this source code is  ")

    ip = input("Display? (Y/N): ")

    if(ip.upper() == 'Y'):
        for w_map in np.procedureStorage:
            np.print_map(w_map)





