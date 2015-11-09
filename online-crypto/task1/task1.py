#!/usr/bin/python
import binascii
import sys
import time
from des import *

def bintohex(s):
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return binascii.hexlify(t).upper()

def bit2str(s):
    '''
    :param s: Input your string of 1s and 0s (must be a string)
    :return: Your binary, but expressed as a character string
    This will often return a garbled result if you are encrypting.
    This will (hopefully) return an English result if you are decrypting
    '''
    t = ''.join(chr(int(s[i:i+8], 2)) for i in xrange(0, len(s), 8))
    return t

def writetodebugger(s):
    f = open('Output.txt', 'a')
    f.write(str(s))
    f.close()

def boolean_to_binary(data):
    integer_array = []
    for i in range(len(data)):
        if data[i] == False:
            integer_array.append(0)
        else:
            integer_array.append(1)

    #writetodebugger(integer_array)

    return integer_array

def str2binaryarray(s):
    '''

    :param s: Input your plaintext message
    :return: an array of 1s and 0s (integers) which represent your characters, with each character getting 8 bits
    '''
    binary_message = []
    for i in range(len(s)):
        binary_representation_of_character = format(ord(s[i]), 'b').zfill(8) #this should fill it in to 8 bits
        # print binary_representation_of_character
        binary_message.append(binary_representation_of_character)

    binary_message = ''.join(binary_message) #merge it all into one nice string

    binary_message_list = list(binary_message) #it should now look like [1, 0, 1, 1, 0.... ]
    binary_message_list = map(int, binary_message_list) #this should convert everything into an int

    return binary_message_list

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
    '''

    :param str1: Array of 1s and 0s (must be integers)
    :param str2: Array of 1s and 0s (must be integers, and also same length)
    :return: XOR'd result, as an array of 1s and 0s (integers)
    '''
    mylogicalarray = []
    for i in range(len(str1)):
        mylogicalarray.append(bool(str1[i]) ^ bool(str2[i]))
    return mylogicalarray

def break_chunks(list1, n):
    for i in xrange(0, len(list1), n):
        yield list1[i:i+n]

def break_list_64bit(list1):
    '''

    :param list1: Provide this method with your array of 1s and 0s (must be integers)
    :return: Returns an array of arrays, with each array holding 64 bits, and also proper padding applied for CBC
    '''

    #this will normalize the array to a special length which is a multiple of 64 bits, with special padding.
    if len(list1)%64 == 0: #if it is a multiple of 64 bits, then I need to append a special thing.
        list1 = list1 + [1] + [0]*63 #append 64 bits of dummy data
    else:
        list1 = list1 + [1] #add 1 as a special starter, because we can
        while len(list1)%64 != 0:
            list1 = list1 + [0]
    array_of_arrays = list(break_chunks(list1, 64))


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

    bytekey = binascii.a2b_hex(key) #convert from hex to bytes
    myDes = des(bytekey) #initialize the DES

    binary_message_list = str2binaryarray(message)
    bin_message_broken_and_padded = break_list_64bit(binary_message_list)


    binary_iv = (bin(int(iv, 16))[2:]).zfill(64) #this converts the initialization vector into a binary list and
    # adds leading 0s to make it 64-bit

    binary_iv_list = list(binary_iv) #convert it into a list
    binary_iv_list = map(int, binary_iv_list) #convert all elements to int so I can actually xor stuff

    ##### EVERYTHING IS READY!!! #######

    cipher_output = []
    cipher_output_string = []

    #this is the CBC implementation
    for i in range(len(bin_message_broken_and_padded)):
        if i == 0:
            initial_xor_message = logical_xor(bin_message_broken_and_padded[i], binary_iv_list)
            cipher1 = myDes.des_encrypt(initial_xor_message)
            cipher_output.append(cipher1)
            cipher_output_string.append("".join(str(x) for x in cipher1))
        else:
            xor_before_cipher = logical_xor(bin_message_broken_and_padded[i], cipher_output[i-1])
            cipher2 = myDes.des_encrypt(xor_before_cipher)
            cipher_output.append(cipher2)
            cipher_output_string.append("".join(str(x) for x in cipher2))
    cipher_output = "".join(cipher_output_string) #unify the strings I think this works

    #The cipher output is going to look like nonsense. We must convert the bits to the str representation
    cipher_output_garbled = bit2str(cipher_output)

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

    bytekey = binascii.a2b_hex(key) #convert from hex to bytes
    myDes = des(bytekey) #initialize the DES

    binary_iv = (bin(int(iv, 16))[2:]).zfill(64) #this converts the initialization vector into a binary list and
    # adds leading 0s to make it 64-bit

    binary_iv_list = list(binary_iv)
    binary_iv_list = map(int, binary_iv_list) #convert all elements to int so I can actually xor stuff

    #get binary form of message
    binary_message_list = str2binaryarray(message)


    binary_message_64bit_array = list(break_chunks(binary_message_list, 64)) #break message up into 64 bit chunks

    cipher_input = []
    plaintext_output_string = []

    #this is the CBC implementation
    for i in range(len(binary_message_64bit_array)):
        if i == 0:
            cipher_input.append(binary_message_64bit_array[i])
            plaintext1_pre_xor = myDes.des_decrypt(binary_message_64bit_array[i])

            plaintext1_post_xor = logical_xor(plaintext1_pre_xor, binary_iv_list)
            integer_array_of_boolean = boolean_to_binary(plaintext1_post_xor)

            plaintext_output_string.append("".join(str(x) for x in integer_array_of_boolean))
        else:
            cipher_input.append(binary_message_64bit_array[i])
            plaintext1_pre_xor = myDes.des_decrypt(binary_message_64bit_array[i])
            plaintext1_post_xor = logical_xor(cipher_input[i-1], plaintext1_pre_xor)
            integer_array_of_boolean = boolean_to_binary(plaintext1_post_xor)
            plaintext_output_string.append("".join(str(x) for x in integer_array_of_boolean))

    plaintext_output_string = "".join(plaintext_output_string) #unify the strings I think this works

    #remove padding
    deleted_a_one = False
    while (not deleted_a_one):
        if plaintext_output_string[-1] == '0':
            plaintext_output_string = plaintext_output_string[:-1]
        elif plaintext_output_string[-1] == '1':
            plaintext_output_string = plaintext_output_string[:-1]
            deleted_a_one = True

    #This will translate our bits back into language that humans can (hopefully) understand
    plaintext_output_cleaned = bit2str(plaintext_output_string)

    return plaintext_output_cleaned

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
