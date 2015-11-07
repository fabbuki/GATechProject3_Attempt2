iv = '3132333435363738'

binary_iv = (bin(int(iv, 16))[2:]).zfill(64)

print binary_iv

print len(binary_iv)

