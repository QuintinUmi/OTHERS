import random
import time



def map_generate(x, y):

    pz_map = [-1]
    num_list_ori = list(range(0, x * y))
    num_list = []
    used = []
    for i in range(len(num_list_ori)):
        used.append(False)

    for i in range(len(num_list_ori)):
        while(len(num_list) < x * y):
            random.seed(time.time())
            r = int(random.random() * x * y)
            if(not used[r]):
                num_list.append(num_list_ori[int(r)])
                used[r] = True
            else:
                continue

    for i in range(1, x + 1):
        temp = [-1]
        for j in range(1, y + 1):
            temp.append(num_list[(i - 1) * y + j - 1])
        pz_map.append(temp)

    return pz_map
    





def map_generate_have_solution(x, y):
    pass




if __name__ == "__main__":
    print(map_generate(8, 8))