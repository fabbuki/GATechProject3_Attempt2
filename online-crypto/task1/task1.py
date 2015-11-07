#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bintohex(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()

def test():
    key1 = b"\0\0\0\0\0\0\0\0"
    key2 = b"\0\0\0\0\0\0\0\2"
    message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    message2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    test_des(key1, message1)
    test_des(key1, message2)
    test_des(key2, message1)
    test_des(key2, message2)

def test_des(key, message):
    k = des(key)
    c = k.des_encrypt(message)
    print bintohex("".join([str(e) for e in c]))

#this performs a simple logical XOR in python
def logical_xor(str1, str2):
    return bool(str1) ^ bool(str2)

def break_chunks(list1, n):
    for i in xrange(0, len(list1), n):
        yield list1[i:i+n]

def break_list_64bit(list1):

    #this will normalize the array to a special length which is a multiple of 64 bits, with special padding.
    if len(list1)%64 == 0: #if it is a multiple of 64 bits, then I need to append a special thing.
        list1 = list1 + [1] + [0]*63 #append 64 bits of dummy data
    else:
        list1 = list1 + [1] #add 1 as a special starter, because we can
        while len(list1)%64 != 0:
            list1 = list1 + [0]
    number_of_64bit_chunks = len(list1)/64 #if this isn't an integer, we've screwed up badly
    array_of_arrays = break_chunks(list1, number_of_64bit_chunks)

    return array_of_arrays #now you have an array of arrays with each array as 64-bit length 1s and 0s.

#assumes the lists are equal in length and all 1s or 0s
def xor_list(list1, list2):
    my_xor_list = []
    for i in range(len(list1)):
        my_xor_list[i] = logical_xor(list1[i], list2[i])

    return my_xor_list

def cbc_encrypt(message, key, iv):

    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    # TODO: Add your code here.

    bytekey = bytearray(key.decode("hex"))
    myDes = des(bytekey)

    #convert message to HEX
    hex_message = binascii.hexlify(message)
    binary_message = bin(int(hex_message, 16))[2:]
    binary_message_list = list(binary_message) #it should now look like [1, 0, 1, 1, 0.... ]

    bin_message_broken_and_padded = break_list_64bit(binary_message_list)

    binary_iv = bin(int(iv, 16))[2:] #this converts the initialization vector into a binary list
    binary_iv_list = list(binary_iv)

    ##### EVERYTHING IS READY!!! #######

    #step 1 is to XOR the first char plaintext with the IV

    cipher_output = []

    for i in range(len(bin_message_broken_and_padded)):
        if i == 0:
            initial_xor_message = logical_xor(bin_message_broken_and_padded[i], binary_iv_list)
            cipher1 = myDes.des_encrypt(initial_xor_message)
            cipher_output[i] = cipher1
        else:
            xor_before_cipher = logical_xor(bin_message_broken_and_padded[i], cipher_output[i-1])
            cipher2 = myDes.des_encrypt(xor_before_cipher)
            cipher_output[i] = cipher2

    #test()
    return ''

def cbc_decrypt(message, key, iv):
    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      plaintext: string
    """
    # TODO: Add your code here.
    test()
    return ''

def main(argv):
    if len(argv) != 5:
        print 'Wrong number of arguments!\npython task1.py $MODE $INFILE $KEYFILE $IVFILE $OUTFILE'
        sys.exit(1)
    mode = argv[0]
    infile = argv[1]
    keyfile = argv[2]
    ivfile = argv[3]
    outfile = argv[4]
    message = None
    key = None
    iv = None
    try:
        message = open(infile, 'r').read()
        key = open(keyfile, 'r').read()
        iv = open(ivfile, 'r').read()
    except:
        print 'File Not Found'
    start = time.time()
    if mode == "enc":
        output = cbc_encrypt(message, key, iv)
    elif mode == "dec":
        output = cbc_decrypt(message, key, iv)
    else:
        print "Wrong mode!"
        sys.exit(1)
    end = time.time()
    print "Consumed CPU time=%f"% (end - start)
    open(outfile, 'w').write(output)

if __name__=="__main__":
    main(sys.argv[1:])
