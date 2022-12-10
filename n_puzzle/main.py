import pdb
import time
import pickle
import npuzzle_map_generator as mg
import npuzzle_map_solve_1m1 as ms

XMAX, YMAX = 8, 8

def main():
    
    unproccessMap = mg.map_generate(XMAX, YMAX)
    time_start = time.time()
    x_max, y_max = len(unproccessMap) - 1, len(unproccessMap[1]) - 1
    np = ms.MapSolve()
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

    input("Press ENTER to show and write the procedure of the solution in a file where the upper level of this source code is  ")

    ip = input("Display? (Y/N): ")

    if(ip.upper() == 'Y'):
        for w_map in np.procedureStorage:
            np.print_map(w_map)

    input("\nPress ENTER to write in file... (Note: The program may not create the file if no Administrator Permissions) ")
    f = open(".\\result.txt", 'w')
    for w_map in np.procedureStorage:
        np.write_res(f, w_map)
    print("", file=f)
    print("--------------------Result---------------------", file=f)
    np.write_res(f, np.pz_map)
    print("-----------------------------------------------", file=f)
    print("Status (0->Success, -1->No Solution): ", res, file=f)
    print("Total Steps: ", len(np.procedureStorage), file=f)
    print("Deepest recursion depth: ", np.max_deep, file=f)
    f.close()

    input("\nPress ENTER to continue...  ")



if __name__ == "__main__":
    main()