import sys
import os
import glob
import fnmatch

#Function needed to make a sprawozdanie
def main(argv):
    if len(argv) != 3:
        print("Error: No arguments")
        return

    path = argv[1]
    strategy = argv[2]
    #depth = argv[3]
    depths = {"01", "02", "03", "04", "05", "06", "07"}

    number_of_files = 0
    avg_of_nodes_visited = 0
    avg_of_nodes_fully_explored = 0
    avg_of_path_lenght = 0
    avg_time = 0
    max_depth = 0

    TOTAL_AVG_TIME =0
    TOTAL_AVG_NODES = 0
    TOTAL_AVG_NODES_VIS =0

    for dep in depths:
        print(dep)
        for file in glob.glob(path + '\\*', recursive=True):
            with open(file) as f:
                if fnmatch.fnmatch(file, '*_' + dep + '_*' + strategy + '_*_stats.txt'):
                    print("Processing file " + str(number_of_files))
                    content = f.readlines()
                    content = [x.strip() for x in content]
                    if int(content[3]) > max_depth:
                        max_depth = int(content[3])
                    avg_time += float(content[4])
                    avg_of_nodes_visited += int(content[1])
                    avg_of_nodes_fully_explored += int(content[2])
                    avg_of_path_lenght += int(content[0])
                    number_of_files += 1
        TOTAL_AVG_TIME += avg_time
        TOTAL_AVG_NODES += avg_of_nodes_visited
        TOTAL_AVG_NODES_VIS += avg_of_nodes_fully_explored

        if not os.path.exists("avgs"):
            os.makedirs("avgs")
        fi = open("avgs/" + strategy + '_' + dep + "_avg.txt", "w+")
        fi.write("TIME: " + str(avg_time / number_of_files) + '\n')
        fi.write("NODES VISITED: " + str(avg_of_nodes_visited / number_of_files) + '\n')
        fi.write("NODES FULLY EXPLORED: " + str(avg_of_nodes_fully_explored / number_of_files) + '\n')
        fi.write("PATH LENGHT: " + str(avg_of_path_lenght / number_of_files) + '\n')
        fi.write("NUMBER OF FILES: " + str(number_of_files) + '\n')
        fi.write("MAX DEPTH: " + str(max_depth) + '\n')

        number_of_files = 0
        avg_of_nodes_visited = 0
        avg_of_nodes_fully_explored = 0
        avg_of_path_lenght = 0
        avg_time = 0
        max_depth = 0

    if not os.path.exists("avgs2"):
        os.makedirs("avgs2")
    fi = open("avgs2/" + strategy + '_' + "_avg.txt", "w+")
    fi.write("TIME: " + str(TOTAL_AVG_TIME / 413) + '\n')
    fi.write("NODES VISITED: " + str(TOTAL_AVG_NODES / 413) + '\n')
    fi.write("PATH LENGHT: " + str(TOTAL_AVG_NODES_VIS / 413) + '\n')


main(sys.argv)
