import des_wrapper
import binascii
import time
import task2

#decrypt ciphertext with key

def convert_to_binary(key):

    binary_current = (bin(int(key, 16))[2:]).zfill(64)
    binary_current = list(binary_current)
    binary_current = map(int,binary_current)

    return binary_current

f = open('ciphertext', 'r')
ciphertext =  f.read()

g = open('plaintext', 'r')
plaintext = g.read()

binary_message = bin(int(binascii.hexlify(plaintext),16))[2:].zfill(64)
binary_message_list = map(int,list(binary_message))

print binary_message_list

#starter key
start = time.time()

currentKey = '8080807580808080' #starter key
binary_current = convert_to_binary(currentKey)
test = des_wrapper.des_encrypt(binary_current, binary_message_list)
number_of_tries = 1

print test == ciphertext

while currentKey != '808080757f7f7f7f':
    currentKey = task2.enum_key(currentKey)
    binary_current = convert_to_binary(currentKey)
    test = des_wrapper.des_encrypt(binary_current, binary_message_list)
    number_of_tries += 1
    if test == ciphertext:
        print "I FOUND IT"
        print currentKey
        print "The magic key precedes this message"
        break

end = time.time()

print number_of_tries
print "Consumed CPU time=%f" % (end - start)


#get starter key and enumerate
#create a DES
#decrypt the cipher
#compare to plaintext