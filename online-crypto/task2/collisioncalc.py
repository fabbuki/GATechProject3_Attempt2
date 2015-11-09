import math

N = 2**56
probUnique = 1.0
for k in xrange(1, 2000):
    probUnique = probUnique * (N - (k - 1)) / N
    prob_collision = 1 - probUnique #1 - math.exp(-0.5 * k * (k - 1) / N)
    #print '{0:.100000f}'.format(prob_collision)

print '{0:.10000f}'.format(2.9*10**-39)

#scaling up the key hacks

seconds_28bit = 20685
print "56 bit"
print (2**56)/(2**28)*seconds_28bit

print "triple DES"
print (2**168)/(2**28)*seconds_28bit

print "AES256"
print (2**256)/(2**28)*seconds_28bit