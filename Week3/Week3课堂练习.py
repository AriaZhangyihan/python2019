
# coding: utf-8

# 课堂练习

# In[12]:


# 元组可变参数示例
def printinfo(var ):
    for i in range(1,var):
        for j in range(i,var):
            print(i,'*',j,'=',i*j)
printinfo(10)

