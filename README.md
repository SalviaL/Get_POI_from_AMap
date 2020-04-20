# Get_POI_from_AMap
从高德地图获取POI数据

各种电子地图作为大型的实时更新的数据库，不好好利用一下怎么可以？正好最近做的论文也是和POI数据相关的（Point of Interest），研究了一波高德地图的POI数据，然后写了个脚本来下载。完整的代码已经上传到GitHub，点击阅读原文可以转跳。这里分享点脚本的核心：

## API申请
在高德开发者平台-个人中心-应用管理中添加新的应用，勾选**Web服务**，可以申请到一个key，这个key在接下来通过url检索的时候将用到。

## 检索url
```java
url_temp = '''
http://restapi.amap.com/v3/place/text?
key=%s&keywords=%s&city=%s
&citylimit=true&children=1&offset=20&
page=%s&extensions=all'''

# 上面这个只是为了方便阅读
# 把url_temp换行显示
# coding时我还是喜欢下面这种一步到位的
url_temp = 'http://restapi.amap.com/v3/place/text?key=%s&keywords=%s&city=%s&citylimit=true&children=1&offset=20&page=%s&extensions=all'
url_example = url_tem % ('<Your Key>','加油站', '长沙市', str(<page>))
```
上面这个字符串是用于检索POI的url，需要提供关键字和城市，关键字和城市可以通过高德的开发者文档(https://lbs.amap.com/api/webservice/guide/api/search/#text)查询。开车总是需要加油的，上面url_example就是在长沙市查询加油站的检索链接。

## 检索
```java
def get_poi_by_url(url)
    url = quote(url, safe='/:?&=')
    html = ""

    with request.urlopen(url) as f:
        html = f.read()
        rr = json.loads(html)
        if total_record == 0:
            total_record = int(rr['count'])
        return rr['pois']
```
这个方法会返回一个json对象，包括city中有关keyword在page页的所有数据。

![我寻思你可以关注一下](https://mmbiz.qpic.cn/mmbiz_png/rXkVB6hSVERndKYb2MIj63YXicbWtBQk350KGicN1iatW799VU5jk0CjVTFtaqoqaCFicTw2p2CibNNu2ia9r4yDUTWQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
