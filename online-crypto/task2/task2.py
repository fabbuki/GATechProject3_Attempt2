#!/usr/bin/python

#my key range: 8080807580808080,808080757f7f7f7f

import sys
import binascii
import time
import des_wrapper

def break_chunks(list1, n):
    for i in xrange(0, len(list1), n):
        yield list1[i:i+n]

def bit2str(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return t

def enum_key(current):
    """Return the next key based on the current key as hex string.


    TODO: Implement the required functions.
    """
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

    #print array_of_arrays

    binary_array = "".join(array_of_arrays)

    next_hex = str(hex(int(binary_array, 2))[2:].rstrip("L"))

    return next_hex

def convert_to_binary(key):

    binary_current = (bin(int(key, 16))[2:]).zfill(64)
    binary_current = list(binary_current)
    binary_current = map(int,binary_current)

    return binary_current

def main(argv):
    if argv[0] == 'enum_key':
        print enum_key(argv[1])
    elif argv[0] == 'crack':

        #load in my ciphertext and plaintext
        f = open('ciphertext_student_247.txt', 'r')
        ciphertext =  f.read()

        g = open('plaintext', 'r')
        plaintext = g.read()

        binary_message = bin(int(binascii.hexlify(plaintext),16))[2:].zfill(64)
        binary_message_list = map(int,list(binary_message))

        start = time.time() #start the count

        #first try (I know, this violates the DON'T-REPEAT-YOURSELF rule)
        currentKey = '8080017580808080' #starter key
        binary_current = convert_to_binary(currentKey)
        test = des_wrapper.des_encrypt(binary_current, binary_message_list)
        test = bit2str(test)
        number_of_tries = 1

        if test == ciphertext:
            print "Found it on the first try! The key is: " + currentKey
        else:
            while currentKey != '8080017580808094':
                currentKey = enum_key(currentKey)
                binary_current = convert_to_binary(currentKey)
                test = des_wrapper.des_encrypt(binary_current, binary_message_list)
                test = bit2str(test)
                number_of_tries += 1
                if test == ciphertext:
                    print "Found it after " + str(number_of_tries) + " tries. The key is: " + currentKey
                    break

        end = time.time()

        print "Consumed CPU time=%f" % (end - start)
        print "Average number per minute = %f" % (number_of_tries/(end-start)*60)

    else:
        raise Exception("Wrong mode!")

if __name__=="__main__":
    main(sys.argv[1:])
