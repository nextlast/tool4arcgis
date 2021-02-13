# -*- coding: utf-8 -*-
import arcpy
import string
import os
err="第{}个要素,点{},创建错误"
msg="导入了{}个要素"
cur=None
try:
    txt=arcpy.GetParameterAsText(0)
    outfc=arcpy.GetParameterAsText(1)
    spatial=arcpy.SpatialReference(4528)
    txtfile=open(txt)
    arcpy.CreateFeatureclass_management(os.path.dirname(outfc),os.path.basename(outfc),"POLYGON","", "", "",spatial)
    arcpy.AddField_management(outfc,"pointno","LONG")
    cur=arcpy.da.InsertCursor(outfc,["SHAPE@"]) 
    arr=arcpy.Array()              
    array=arcpy.Array()

    featno=0
    ringid=-1
    featid=-1

    for line in txtfile.readlines():
        values = line.replace("\n", "").replace("\r", "").split(",")
        if len(values) >= 9 and values[len(values)-1].strip() == "@" and featno== 0:
            featno+=1
            ringid=-1

        elif len(values) ==4 and featno>=1:
            if ringid==-1:
                ringid=values[1]
            if ringid!=values[1]:
                array.add(arr)
                arr.removeAll()
            p=arcpy.Point()
            try:
                p.X=values[3]
                p.Y=values[2]
            except:
                raise Exception,err
            arr.add(p)
            ringid=values[1]

        elif len(values) >= 9 and values[len(values)-1].strip() == "@" and featno>=1:
            array.add(arr)
            cur.insertRow([arcpy.Polygon(array)])
            array.removeAll()
            arr.removeAll()
            featno +=1
            ringid=-1

        elif len(values) == 6:
            if featid==-1:
                featid=values[1]
		featno+=1
	    if ringid==-1:
                ringid=values[2]
            if featid==values[1] and ringid!=values[2]:
                array.add(arr)
                arr.removeAll()
            if featid!=values[1]:
                array.add(arr)
                cur.insertRow([arcpy.Polygon(array)])
                array.removeAll()
                arr.removeAll() 
                featno+=1   
            p=arcpy.Point()
            try:
                p.X=values[5]
                p.Y=values[4]
            except:
                raise Exception,err
            arr.add(p)
            ringid=values[2]
            featid=values[1]

    array.add(arr)
    cur.insertRow([arcpy.Polygon(array)])
    array.removeAll()
    arr.removeAll()
    arcpy.AddMessage(msg.format(featno))

except Exception as e:
    if str(e)==err:
        err=err.format(featno,values[0])
        arcpy.AddError(err)
    elif str(e)!="":
        arcpy.AddError(str(e))
    arcpy.AddError(arcpy.GetMessages(2))
finally:
    if cur:
        del cur
    if txtfile:
        txtfile.close()
