# Initialize the series with a given second element
given_num = 100
const = 1.0003

# First tuple
first_elem = given_num / const
second_elem = round(first_elem * const, 4)
first_tuple = (round(first_elem, 4), given_num, None)

# Second and subsequent tuples
num_tuples = 5
series = [first_tuple]
for i in range(num_tuples - 1):
    print("tuple number:", i)
    prev_second = series[-1][1]
    print("prev_second", prev_second)
    print("series -1 ", series[-1])
    curr_first = prev_second
    curr_second = round(curr_first * const, 4)
    series.append((round(curr_first, 4), curr_second, None))
    print("")

# Add third element to tuples
for i in range(num_tuples - 1):
    curr_first = series[i][0]
    next_second = series[i+1][1]
    curr_third = round(curr_first / next_second, 4)
    series[i] = (series[i][0], series[i][1], curr_third)
series[-1] = (series[-1][0], series[-1][1], None)

# Print series
print("Series:")
for tup in series:
    print(tup)
