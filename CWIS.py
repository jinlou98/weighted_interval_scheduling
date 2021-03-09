# Hannah Catabia, catabia@bu.edu
# Solution code for PA2, CS330 Fall 2020
# Adapted from:
# Gavin Brown, grbrown@bu.edu
# CS330 Fall 2019, Programming Exercise Solution 

# Name: Jin Lou


import sys


############################

# DO NOT CHANGE THIS PART!!

############################

def readInput(input_file):
    with open(input_file, 'r') as f:
        raw = [[float(x) for x in s.split(',')] for s in f.read().splitlines()]
        # number of intervals
        N = int(raw[0][0])
        # max number to schedule
        k =  int(raw[1][0])
        # intervals, with name of interval as an int
        intervals = raw[2:]

        for i in range(len(intervals)):
            intervals[i][0] = int(intervals[i][0])
        return N, k, intervals
    

def writeOutput(schedule, output_file):
    with open(output_file, 'w') as f:
        for i in schedule:
            f.write(str(i) + '\n')


def Run(input_file, output_file):
    N, k, intervals = readInput(input_file)
    schedule = find_solution(N, k, intervals)
    assert all(isinstance(n, int) for n in schedule), "All items in schedule array should be type INT, otherwise the autograder will fail."
    writeOutput(schedule, output_file)


############################

# ADD YOUR OWN METHODS HERE
# (IF YOU'D LIKE)

############################

# computer array p
# p[j] stores last compatible interval for finish_index j
# running time O(nlogn)
def compute_p(finish):
    #create array p
    P = [0] * len(finish)

    for i in reversed(range(len(finish))):      #O(n)
        # bound that we search
        low = 0
        high = i - 1
        best = -1

        # start binary search
        while(low <= high):                     #O(logn)
            mid = (low + high) // 2

            # not compatible
            if(finish[mid][2] > finish[i][1]):
                high = mid - 1

            # compatible but not sure if its the last compatible
            # need to compare the gap
            elif(finish[mid][2] <= finish[i][1]):
                best = mid
                low = mid + 1

        P[i] = best
        # testing
        # print("3")
        # print(P[i])

    # testing        
    # print()
    # print(*P, sep=', ')

    return P



############################

# FINISH THESE METHODS

############################

def find_solution(N, k, intervals):
    # You are given the following variables:
    # N - the total number of intervals
    # k - the max number of intervals you can put on your schedule
    # intervals - a list of lists
    # ---> Each sublist in intervals has 4 items representing one interval:
    # ---> 0) an INT that is the NAME of the interval
    # ---> 1) a float that is the start time of the interval
    # ---> 2) a float that is the end time of the interval
    # ---> 3) a float that is the weight of an interval

    intervals.sort(key=lambda x: x[2])  # sort jobs in increasing finishing time
    # b = intervals.copy()    # copy the original list
    # b.sort(key=lambda x: x[1])  #list with jobs in increasing starting time

    # testing
    # print ("Test print list \"intervals\"")
    # for x in range(len(intervals)):
    #     print (intervals[x])


    P = [0] * N
    # print ()
    # print ("Test print empty p(j)")
    # for x in range(len(P)):
    #     print (P[x])


    # compute array P(j)
    P = compute_p(intervals)

    # create a list containing N+1 lists, each of k+1 items
    M = [[0 for i in range(k+1)] for j in range(N+1)]  # max income
    B = [[0 for i in range(k+1)] for j in range(N+1)]  # backtracing


    # base case
    for i in range(N+1):
        M[i][0] = 0
    for j in range(k+1):    
        M[0][j] = 0

    # fill OPT table
    for i in range(0,N):
        for j in range(0,k):
            # if pick the interval, we add weight of current interval and M[p[j]]
            # if not pick the interval, we add previous M[]
            if (intervals[i][3] + M[P[i]][j-1] > M[i-1][j]):
                M[i][j] = intervals[i][3] + M[P[i]][j-1]
                B[i][j] = 1
            else:
                M[i][j] = M[i-1][j]
                B[i][j] = 0
                

    # return a list called schedule
    # each element in schedule should be 
    # an INT representing the NAME of an interval
    # you would like to place on your schedule
    schedule =[]

    # backtracing
    while (i > -1 and j > -1):
        if (B[i][j] == 1):
            # if interval not there, append it
            if(intervals[i][0] not in schedule):
                schedule.append(intervals[i][0])
                i = P[i]
                j = j - 1

        else:
            i = i - 1
            # j remain same

    return schedule




############################################

# CHANGE INPUT FILES FOR DEBUGGING HERE

############################################

def main(args=[]):
    # WHEN YOU SUBMIT TO THE AUTOGRADER, 
    # PLEASE MAKE SURE THE FOLLOWING FUNCTION LOOKS LIKE:
    # Run('input', 'output')
    # Run('input_student_example_10_4', 'output_my_10_4')
    # Run('input_student_example_10_8', 'output_my_10_8')
    # Run('input_student_example_20_2', 'output_my_20_2')
    # Run('input_student_example_10_7', 'output_my_10_7')
    # Run('input_student_example_10_8', 'output_my_10_8')
    Run('input', 'output')

if __name__ == "__main__":
    main(sys.argv[1:])    

