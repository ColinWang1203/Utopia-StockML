import functools

list1 = ['20191206', '20191209']
list2 = ['20191206', '20191209']
if not functools.reduce(lambda i, j : i and j, \
            map(lambda m, k: m == k, list1, list2), True) :
    print('not identical') 
else:
    print('identical')
        
