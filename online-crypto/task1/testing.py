import des
import binascii

hexkey = "3132333435363738"
key1 = b"\0\0\0\0\0\0\0\0"

key2 = binascii.a2b_hex(hexkey)

hexkey1 = binascii.b2a_hex(key1)

print hexkey1

print binascii.a2b_hex(hexkey1)

print key2

print type(key2)

iv = '3132333435363738'

binary_iv = (bin(int(iv, 16))[2:]).zfill(64)

print binary_iv

print len(binary_iv)




#my shit

f = open('ciphertext_2','r')
myciphertextfromfile = f.read()
f.close()

print myciphertextfromfile
print type(myciphertextfromfile)
print len(myciphertextfromfile)


print 'HELLO'
ciphertext = b'11011001011010101100110011001001111100011111010110110101000011001100111110010011010010100000011011010110011100011011010010011110001000110000111110111011001001101001010110111100000011101011001001010110010000000100101000001010100011000001000101000011110110111111011010011101010110111001110001001101101111011101001000100111'
print ciphertext
print type(ciphertext)
print len(ciphertext)