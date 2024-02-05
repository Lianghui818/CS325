import math
import re

def min_band_length(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        m = int(file.readline().strip())
        # P = [tuple(map(int,point.strip("()").split(','))) for point in file.readline().strip().split(',')]
        input_line1 = file.readline().strip()
        points = re.findall(r'\((-?\d+),(-?\d+)\)', input_line1)
        P = [tuple(map(int, match))for match in points]
        n = int(file.readline().strip())
        # Q = [tuple(map(int,point.strip("()").split(','))) for point in file.readline().strip().split(',')]
        input_line2 = file.readline().strip()
        points = re.findall(r'\((-?\d+),(-?\d+)\)', input_line2)
        Q = [tuple(map(int, match))for match in points]
        t = int(file.readline().strip())
        L = list(map(int, file.readline().strip().split(',')))

        print (P, Q)

    shortest_band = find_shortest_band(P, Q, m, n, L)
    with open(output_file_path, 'w') as file:
        file.write(str(shortest_band))

def distance (p, q):            # p, q: two points, the coordinates of p are (p[0],p[1]),The coordinates of q are (q[0],q[1])
    d = math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)
    return d

def check_usability(P, Q, m, n, length):
    # create a Dynamic Programming Matrix
    DPM =[[0]*(n+1) for _ in range (m+1)]
    # DPM[i][j] = 1: in length L, Pfrog can get point P and Qfrog can get point Q
    DPM[0][0] = 1           # when P, Q both at staring point, True

    for i in range(1, m+1):
        for j in range(1, n+1):
            if i > 0:
                DPM[i][j] |= DPM[i-1][j] and distance(P[i-1], Q[j-1]) <= length
            if j > 0:
                DPM[i][j] |= DPM[i][j-1] and distance(P[i-1], Q[j-1]) <= length
            if i > 0 and j > 0:
                DPM[i][j] |= DPM[i-1][j-1] and distance(P[i-1], Q[j-1]) <= length
    return DPM[m][n]

def find_shortest_band(P, Q, m, n, L):
    L.sort()
    left = 0
    right = len(L) - 1
    shortest_band = -1  # Default value: no band is useful.

    while left <= right:
        mid = (left + right) // 2
        if check_usability(P, Q, m, n, L[mid]):
            shortest_band = L[mid]
            right = mid - 1  # Search in the left half.
        else:
            left = mid + 1  # Search in the right half.

    return shortest_band

input_file_path = 'C:/Users/Administrator/Desktop/input.txt'
output_file_path = 'C:/Users/Administrator/Desktop/output.txt'
min_band_length(input_file_path, output_file_path)

