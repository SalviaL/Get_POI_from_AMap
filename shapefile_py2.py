'''
@Author: 鲁伟鹏
@Date: 2020-04-19 09:16:29
@LastEditTime: 2020-04-22 23:20:29
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \AMap\shapefile_py2.py
@Attention: this file is based on python2 python2 python2 python2
'''
import arcpy
import os
import json
from GCJ02_WGS84 import gcj02towgs84


def create_point_shapefile(file_path):
    arcpy.AddField_management(,)
    arcpy.CreateFeatureclass_management(r'D:\AMap\data_index\shapefile', file_path, "POINT",
                                        r'D:\AMap\data_index\temp.shp', "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", arcpy.SpatialReference(4326))


json_root = 'D:/AMap/data_index/jsonfile'
shp_root = 'D:/AMap/data_index/shapefile'
field = ['id', 'biz_type', 'name', 'type', 'address', 'tel', 'lon',
         'lat', 'pcode', 'pname', 'citycode', 'cityname', 'adcode', 'adname']
type_long = ['pcode', 'citycode', 'adcode']
type_float = ['lon', 'lat']
for cnt, json_file in enumerate(os.listdir(json_root)):
    print cnt+1, '/', len(os.listdir(json_root))
    json_name = json_file[:-5]
    fp = open(json_root + '/' + json_file, 'r')
    points = json.loads(fp.read())
    for re in points:
        re['lon'] = re['location'].split(',')[0]
        re['lat'] = re['location'].split(',')[1]
    create_point_shapefile(json_name+'.shp')
    cursor = arcpy.InsertCursor(shp_root+'/'+json_name+'.shp')
    for i in range(len(points)):
        values = points[i]
        feature = cursor.newRow()
        lon, lat = gcj02towgs84(float(values['lon']), float(values['lat']))
        pt = arcpy.Point(lon, lat)
        feature.setValue('shape', pt)
        for j in range(len(field)):
            field_ = field[j]
            if field_ not in values.keys():
                continue
            if values[field_] == '' or values[field_] == []:
                continue
            if field_ in type_long:
                feature.setValue(field_, int(values[field_]))
            elif field_ in type_float:
                feature.setValue(field_, float(values[field_]))
            else:
                feature.setValue(field_, values[field_])
        cursor.insertRow(feature)
