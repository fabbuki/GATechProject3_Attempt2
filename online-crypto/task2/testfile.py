def break_chunks(list1, n):
    for i in xrange(0, len(list1), n):
        yield list1[i:i+n]


current = '8080807580808080'

binary_current = (bin(int(current, 16))[2:]).zfill(64)

print binary_current

array_of_arrays = list(break_chunks(binary_current,8))

print array_of_arrays

for i in range(len(array_of_arrays)):
    list_version = list(array_of_arrays[i])
    del(list_version[0]) #remove parity bit
    string_version = "".join(list_version)
    array_of_arrays[i] = string_version

print array_of_arrays