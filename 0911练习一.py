
# coding: utf-8

# # 练习一

# In[1]:


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
