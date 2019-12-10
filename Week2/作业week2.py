
# coding: utf-8

# # 课后作业

# 1.计算10000以内所有2,3,4,5的倍数的正整数的和并分别打印出来

# In[38]:


a=0
b=0
c=0
d=0
for s in range(0,10001):
    if(s%2==0):
        a+=s
    if(s%3==0):
        b+=s
    if(s%4==0):
        c+=s
    if(s%5==0):
        d+=s
print(a,b,c,d)


# 2.将可打印的ascii码全部放入一个数组中，并以每行20个的格式打印出来 

# In[68]:


l=[]
for i in range(255):
    d=ord('0')+i
    a=chr(d)
    l.append(a)

for j in range(255):
    print(l[j],end = " ")
    if(j%20==0):
        print('\n')

