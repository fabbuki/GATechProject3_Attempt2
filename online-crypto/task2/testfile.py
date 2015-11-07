def break_chunks(list1, n):
    for i in xrange(0, len(list1), n):
        yield list1[i:i+n]


current = "808080808080b05e"

binary_current = (bin(int(current, 16))[2:]).zfill(64)

#print binary_current

array_of_arrays = list(break_chunks(binary_current,8))

#print array_of_arrays

for i in range(len(array_of_arrays)):
    list_version = list(array_of_arrays[i])
    del(list_version[0]) #remove parity bit
    string_version = "".join(list_version)
    array_of_arrays[i] = string_version

#print array_of_arrays

binary_string = "".join(array_of_arrays)

binary_string_plus_one = bin(int(binary_string,2) + int('1',2))[2:].zfill(56)

#print binary_string_plus_one

#parity time

array_of_arrays = list(break_chunks(binary_string_plus_one, 7)) #break it into 8 pieces of 7

#print array_of_arrays

for i in range(len(array_of_arrays)):
    list_version = list(array_of_arrays[i])
    count_ones = list_version.count('1')

    if count_ones % 2 == 0:
        list_version = ['1'] + list_version
    else:
        list_version = ['0'] + list_version

    array_of_arrays[i] = "".join(list_version)

print array_of_arrays

binary_array = "".join(array_of_arrays)

next_hex = str(hex(int(binary_array, 2))[2:].rstrip("L"))

print next_hex