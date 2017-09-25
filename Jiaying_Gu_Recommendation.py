import sys
import json
import operator
from collections import Counter

def get_matrix(matrix):
    # mtx: {Username: list of movies}
    mtx={}
    for line in matrix:
        user = json.loads(line)
        mtx[(user[0].encode('utf-8'))]=user[1]
    return mtx

def get_lsh(lshash):
    # lsh: [candidate pairs]
    lsh=[]
    for line in lshash:
        candidate_pair=json.loads(line)
        lsh.append([candidate_pair[0].encode('utf-8'),candidate_pair[1].encode('utf-8')])
    return lsh

# Find Jaccard Similarity of two lists
def find_js(user1,user2):
    intersection = set(user1).intersection(set(user2))
    union = set(user1).union(set(user2))
    return float(len(intersection))/len(union)

# Find top5 similar users of all users
def top5(matrix,lshash):
    # top: {User: [top5 similar users]}
    top={}
    for user in matrix.keys():
        c={}
        similar=[]
        for cp in lshash:
            if user in cp:
                c[[x for x in cp if x != user][0]]=find_js(matrix[cp[0]],matrix[cp[1]])

        # Sort similar users by JS
        sorted_js = sorted(c.items(), key=operator.itemgetter(1),reverse=True)

        # Return top 5 similar users
        # Can more than 5 users if JS are the same
        for i in sorted_js:
            if len(sorted_js)>5:
                if i[1]>=sorted_js[4][1]:
                    similar.append(i[0])
            else:
                similar.append(i[0])
            if similar:
                top[user]=similar
    return top

def recommend3(similar_user,matrix):
    rec3=[]
    for user in similar_user.keys():
        mov=[]
        for u2 in similar_user[user]:
            for m in matrix[u2]:
                mov.append(m)
        # Counter: count how many times a movie being watched by similar users
        # Condition 1: being watched for >= 3 times
        # Condition 2: not watched by U
        mov=[m for m in Counter(mov) if Counter(mov)[m]>=3 and m not in matrix[user]]
        if mov:
            rec3.append([user,mov])
    return rec3

if __name__ == '__main__':
    # mtx: movie user matrix
    mtx = open(sys.argv[1])
    # lsh: similar user pairs
    lsh = open(sys.argv[2])

    matrix=get_matrix(mtx)
    lshash=get_lsh(lsh)
    top=top5(matrix,lshash)
    recommend=recommend3(top,matrix)

    for i in recommend:
        print i