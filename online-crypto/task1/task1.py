#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bintohex(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()

#binary to str converter helper

def bit2str(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return t

def test():
    key1 = b"\0\0\0\0\0\0\0\0"
    key2 = b"\0\0\0\0\0\0\0\2"
    # print type(key1)
    # print key1
    message1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    message2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]

    # print "message 1 contains type of"
    # print type(message1[0])

    test_des(key1, message1)
    test_des(key1, message2)
    test_des(key2, message1)
    test_des(key2, message2)

def test_des(key, message):
    k = des(key)
    c = k.des_encrypt(message)
    # print "DES returns type of string:"
    # print type(c)
    # print bintohex("".join([str(e) for e in c]))

#this performs a simple logical XOR in python
def logical_xor(str1, str2):
    mylogicalarray = []

    # print "LOGICAL XOR"
    # print str1
    # print len(str1)
    # print str2
    # print len(str2)

    for i in range(len(str1)):
        mylogicalarray.append(bool(str1[i]) ^ bool(str2[i]))
    return mylogicalarray

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
    #number_of_64bit_chunks = len(list1)/64 #if this isn't an integer, we've screwed up badly
    #print number_of_64bit_chunks
    array_of_arrays = list(break_chunks(list1, 64))
    #print type(array_of_arrays)

    return array_of_arrays #now you have an array of arrays with each array as 64-bit length 1s and 0s.

def cbc_encrypt(message, key, iv):

    """
    Args:
      message: string, bytes, cannot be unicode
      key: string, bytes, cannot be unicode
    Returns:
      ciphertext: string
    """
    # TODO: Add your code here.
    #test()

    bytekey = binascii.a2b_hex(key) #convert from hex to bytes
    # print bytekey
    # print type(bytekey)
    #string_bytekey = str(bytearray(bytekey)) #convert bytearray to a string, so we can use DES methods
    # print string_bytekey
    # print type(string_bytekey)
    myDes = des(bytekey) #initialize the DES

    # #convert message to HEX
    # hex_message = binascii.hexlify(message) #convert message to HEX
    # binary_message = bin(int(hex_message, 16))[2:] #convert HEX to binary

    #take in message, and go character by character and create 8-bit binary and then glue shit together
    binary_message = []
    for i in range(len(message)):
        binary_representation_of_character = format(ord(message[i]), 'b').zfill(8) #this should fill it in to 8 bits
        # print binary_representation_of_character
        binary_message.append(binary_representation_of_character)

    binary_message = ''.join(binary_message) #merge it all into one nice string

    binary_message_list = list(binary_message) #it should now look like [1, 0, 1, 1, 0.... ]
    binary_message_list = map(int, binary_message_list) #this should convert everything into an int

    # print "message broken and padded:"
    bin_message_broken_and_padded = break_list_64bit(binary_message_list)
    # print type(bin_message_broken_and_padded)
    # print bin_message_broken_and_padded

    binary_iv = (bin(int(iv, 16))[2:]).zfill(64) #this converts the initialization vector into a binary list and
    # adds leading 0s to make it 64-bit
    # print binary_iv

    binary_iv_list = list(binary_iv)
    binary_iv_list = map(int, binary_iv_list) #convert all elements to int so I can actually xor stuff

    #binary_iv_list = [0] + binary_iv_list #jenky padding method to make it a 64 bit array
    # print binary_iv_list

    # #sanity check
    # print "binary iv list type is"
    # print type(binary_iv_list[0])
    # print "message list type is"
    # print type(binary_message_list[0])

    ##### EVERYTHING IS READY!!! #######

    #step 1 is to XOR the first char plaintext with the IV

    cipher_output = []
    cipher_output_string = []

    for i in range(len(bin_message_broken_and_padded)):
        if i == 0:
            initial_xor_message = logical_xor(bin_message_broken_and_padded[i], binary_iv_list)
            # print initial_xor_message
            # print type(initial_xor_message)
            # print type(initial_xor_message[0])
            cipher1 = myDes.des_encrypt(initial_xor_message)
            # print type(cipher1)
            # text_file = open("Output.txt", "w")
            # text_file.write(cipher1)
            # text_file.close
            # print "cipher length"
            # print len(cipher1)
            cipher_output.append(cipher1)
            cipher_output_string.append("".join(str(x) for x in cipher1))
            #cipher_output_byte.append(bintohex("".join([str(e) for e in cipher1])).decode("hex")) #just following the way test_des does it
        else:
            xor_before_cipher = logical_xor(bin_message_broken_and_padded[i], cipher_output[i-1])
            cipher2 = myDes.des_encrypt(xor_before_cipher)
            cipher_output.append(cipher2)
            cipher_output_string.append("".join(str(x) for x in cipher2))
            #cipher_output_byte.append(bintohex("".join([str(e) for e in cipher2])).decode("hex")) #yolo
    # print "HELLO HELLO"
    #
    # print type(cipher_output)
    # print type(cipher_output[1])
    cipher_output = "".join(cipher_output_string) #unify the strings I think this works

    # print cipher_output

    cipher_output_garbled = bit2str(cipher_output)

    f = open('Output.txt', 'w')
    f.write(cipher_output_garbled)
    f.close()

    return cipher_output_garbled

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
