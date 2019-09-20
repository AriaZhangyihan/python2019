
# coding: utf-8

# # 练习一

# In[2]:


a=[]
l=[]
for i in range(26):
    d=ord('A')+i
    x=ord('a')+i
    a=[chr(d),chr(x)]
    b=tuple(a)
    l.append(b)

for j in range(26):
    print(l[j][0],"-",l[j][1])


# # 练习二

# In[50]:


import os
suffix='./test'
letters=[str(i)  for i in range(50)]

c=[suffix+l  for l in letters]
path = r'D:\test'
path = r'D:\test'
for t in c:
    os.makedirs(path + t)

