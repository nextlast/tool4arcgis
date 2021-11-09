# -*- coding: utf-8 -*-
import arcpy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def u2g(str):
    return str.decode('utf-8').encode('gbk')

def getlst(row):

    lst=[]

    partno=1

    for part in row[1]:
        startno=1
        showno=startno
        
        for point in part:
            if point:
                lst.append([showno,partno,point.Y,point.X])
            else:
                lastof=len(lst)-1
                lst[lastof][0]=startno
                startno=showno
                showno-=1
                partno+=1
            showno+=1
        lastof=len(lst)-1
        lst[lastof][0]=startno   
        partno=(partno//100+1)*100+1
    return lst


shpfile=arcpy.GetParameterAsText(0)
txt=arcpy.GetParameterAsText(1)
fo=open(txt,'w')

a1="[属性描述]\n"
a2="坐标系=2000国家大地坐标系\n"
a3="几度分带=3\n"
a4="投影类型=高斯克吕格\n"
a5="计量单位=米\n"
a6="带号=40\n"
a7="精度=0.0100\n"
a8="转换参数=,,,,,,\n"
a9="[地块坐标]\n"


fo.write(u2g(a1+a2+a3+a4+a5+a6+a7+a8+a9))
for row in arcpy.da.SearchCursor(shpfile,["OID@","SHAPE@"]):

    fo.write("{},{},{},{},{},,,,@\n".format(row[1].pointCount,int(row[1].area),row[0],row[0],u2g("面")))
    lst=getlst(row)
    for a in lst:
	fo.write("{},{},{},{}\n".format(a[0],a[1],a[2],a[3]))

fo.flush()
fo.close()
