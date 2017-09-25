import sys
import json

# Because movies numbered from 0-99, row number x == movie number
# Otherwise we should give each movie a row number
def min_hash(i, sig):
    hash_i = [((3*x)+i) % 100 for x in sig]
    return min(hash_i)

def get_min_hash(mtx):
    # mhash: [Username, [signatures for each hash function]]
    mhash=[]

    for line in mtx:
        user = json.loads(line)

        # Try to change data type right after loading
        # Single quotes, not double quotes
        new_user = [user[0].encode('utf-8'), user[1]]

        mhash.append([new_user[0],[min_hash(i,new_user[1]) for i in range(1,21)]])

    return mhash

def lsh(mhash):
    candidate_pairs=[]
    num_row=4

    for i in range(0,len(mhash)):
        for j in range(i+1,len(mhash)):
            for r in range(0,20,num_row):
                if mhash[i][1][r:r+num_row]==mhash[j][1][r:r+num_row]:
                    candidate_pairs.append([mhash[i][0],mhash[j][0]])
                    break

    # Sort every pair in alphabetic order
    for i in range(0,len(candidate_pairs)):
        candidate_pairs[i]=sorted(candidate_pairs[i])

    return candidate_pairs

if __name__ == '__main__':
    # mtx: movie user matrix
    mtx = open(sys.argv[1])

    for cp in lsh(get_min_hash(mtx)):
        print cp