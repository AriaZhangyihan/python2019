
# coding: utf-8

# In[9]:


Big=(1,3,5,7,8,10,12)#31日的大月列表

def Runyear(year):
    i =False
    if(year%4==0 and year%100!=0) or year%400==0:#判断是否为闰年
        i = True
    return i

def cal(year,month):
    sum = 0
    base=1990
    while base < year-1:
        base +=1
        if Runyear(base):
            sum+=366
        else:
            sum+=365

    base_month=1
    while base_month<month:
        if base_month in Big:
                sum += 31
        elif base_month==2:
            if Runyear(year):
                sum+=29
            else:
                sum+=28
        else:
            sum+=30
        base_month+=1

    return sum

def printcalender(sum,year,month):
    week=(sum+1)%7
    if month in Big:
        day=31
    elif month==2:
        if Runyear(year):
            day=29
        else:
            day=28
    else:
        day=30

    print("日\t一\t二\t三\t四\t五\t六")
    count = 0
    space = 0
    while space<=week:
        space+=1
        count+=1
        print("\t",end="")
        if count%7==0:
            print("\n",end="")
    days=1
    while days<=day:
        print(days,"\t",end="")
        days+=1
        count+=1
        if count %7 ==0:
            print("\n")
def main():
    year =int( input("year="))
    for month in range(1,13):
        print("\n\n第",month,"月\n")
        sums=cal(year,month)
        printcalender(sums,year,month)
        

if __name__=="__main__":
    while True:
        main()
        break

