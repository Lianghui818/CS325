'''
    This file contains the template for Assignment1.  For testing it, I will place it
    in a different directory, call the function <number_of_allowable_intervals>, and check
    its output. So, you can add/remove  whatever you want to/from this file.  But, don't
    change the name of the file or the name/signature of the following function.

    Also, I will use <python3> to run this code.
'''

from sortedcontainers import SortedList

def number_of_allowable_intervals(input_file_path, output_file_path):
    '''
        This function will contain your code.  It wil read from the file <input_file_path>,
        and will write its output to the file <output_file_path>.
    '''
    with open(input_file_path, 'r') as file:
        n, t_min, t_max = map(int, file.readline().strip().split(','))
        A = list(map(int, file.readline().strip().split(',')))

    result_number = count_subarrays(A, t_min, t_max)
    with open(output_file_path, 'w') as file:
        file.write(str(result_number))

def count_subarrays(A, t_min, t_max):
    # O(n**3):
    # left = count = 0
    # for left in range(len(A)):
    #     for right in range(left, len(A)):
    #         if t_min <= sum(A[left:right+1]) <= t_max:
    #             count += 1
    # return count
    pre_sum = 0
    valid_subarr_count = 0
    sorted_sums = SortedList([0])  

    for i in A:
        pre_sum += i
        valid_subarr_count  += sorted_sums.bisect_right(pre_sum - t_min) - sorted_sums.bisect_left(pre_sum - t_max)
        sorted_sums.add(pre_sum)

    return valid_subarr_count 


# Example usage
input_file_path = '/Users/lianghui/Downloads/cs325_algorithm/tests/test_10.txt'
output_file_path = '/Users/lianghui/Downloads/cs325_algorithm/output.txt'
number_of_allowable_intervals(input_file_path, output_file_path)

