import hashlib
import pprint

numblocks = 5
blockcount = 10

hash = hashlib.sha512()
hash.update("This is my not-yethashed text")
hexdigest = hash.hexdigest()

hashes = []
for i in range(0,numblocks):
    #Get 1/numblocks of the hash
    blocksize = (len(hexdigest) / numblocks)
    currentstart = (1 + i) * blocksize - blocksize
    currentend = (1 +i) * blocksize
    hashes.append(int(hash.hexdigest()[currentstart:currentend],16))

pprint.pprint(hashes)
for h in hashes:
    print h % 10
