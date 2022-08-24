import random

# for i in range(10):
# 	print(random.randint(0, 9))

"""opening keys set: index of key_list"""
cut_list = list(random.sample(range(10), 5))

test = bytearray(cut_list)
print(test)

"""evaluation keys set: index of key_list"""
# choose_set = index_set.difference(cut_set)

# D1 = {1:'a', 2:'b', 3:'c'} 
# D2 = {4:'d', 5:'e', 6:'f'} 

# for (k,v), (k2,v2) in zip(D1.items(), D2.items()):
#     print(k, v)
#     print(k2, v2)

# for k, j in zip(D1.keys(), D2.keys()):
#    print(k, D1[k])
#    print(j, D2[j])