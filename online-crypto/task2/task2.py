#!/usr/bin/python

#my key range: 8080807580808080,808080757f7f7f7f

import sys
import binascii

def enum_key(current):
    """Return the next key based on the current key as hex string.


    TODO: Implement the required functions.
    """
#convert to bits
    binary_current = (bin(int(current, 16))[2:]).zfill(64)
#split into 8 sections
#kill highest bit in each


    print next
    return next

def main(argv):
    if argv[0] == 'enum_key':
        print enum_key(argv[1])
    elif argv[0] == 'crack':
        """TODO: Add your own code and do whatever you do.
        """
    else:
        raise Exception("Wrong mode!")

if __name__=="__main__":
    main(sys.argv[1:])
