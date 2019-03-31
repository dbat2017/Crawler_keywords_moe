import urllib.request, re
import pymysql

#默认页码为1
page = 1
flag = 1
#头文件
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}
data = None

#测试是否为空
def test():
    #http://www.moe.gov.cn/was5/web/search?channelid=255182&searchword=%E6%96%B0%E5%B7%A5%E7%A7%91&andsen=%E6%96%B0%E5%B7%A5%E7%A7%91&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME%2CRELEVANCE&page=2
    searchurl = 'http://www.moe.gov.cn/was5/web/search?channelid=255182&searchword=%E6%96%B0%E5%B7%A5%E7%A7%91&andsen=%E6%96%B0%E5%B7%A5%E7%A7%91&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME%2CRELEVANCE&page=' + str(page)
    req = urllib.request.Request(url = searchurl, data = data, headers = headers, method = 'GET')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    txt = re.compile('<h2><a href=(.*?)</h2></dt>', re.S)
    return (''.join(txt.findall(html)))

#写入mysql数据库函数
def mysql_write(url_list, title_list, addtime):
    i = 1
    global flag
    # 连接mysql数据库
    # 打开数据库连接,地址、用户、密码、库名
    db = pymysql.connect("localhost", "root", "root", "xgk")
    cursor = db.cursor()
    # 首先进行数据重复性判断，通过链接地址进行判断
    for i in range(len(url_list)):
        if (check_select(flag) == 1):
            #更新：update table1 set field1=value1 where 范围
            sql = 'update moe_gov_cn set title="%s", url="%s", datetime="%s" where id=%d' % (
                pymysql.escape_string(str(title_list[i])), url_list[i], addtime[i], flag)
        else:
            #插入：insert into table1(field1,field2) values(value1,value2)
            #单引号、双引号转义使用pymysql.escape_string()
            sql = 'insert into moe_gov_cn(ID,title,url,datetime) values(%d, "%s", "%s", "%s")' % (
                flag, pymysql.escape_string(str(title_list[i])), url_list[i], addtime[i])
        cursor.execute(sql)
        i = i + 1
        flag = flag + 1
    db.close()

#已有数据重复性判断
def check_select(flag):
    db = pymysql.connect("localhost", "root", "root", "xgk")
    cursor = db.cursor()
    sql = "select * from moe_gov_cn where id=%d" % (flag)
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()
    return (len(cursor.fetchall()))

#页面代码数据获取，正则匹配
def request():
    global page
    searchurl = 'http://www.moe.gov.cn/was5/web/search?channelid=224838&searchword=%E6%96%B0%E5%B7%A5%E7%A7%91&andsen=%E6%96%B0%E5%B7%A5%E7%A7%91&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME%2CRELEVANCE&page=' + str(page)
    req = urllib.request.Request(searchurl, data, headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    #print(html)

    #正则匹配
    #根据“h2”获取title和url信息
    title_and_url = re.compile('<h2><a href=(.*?)</h2></dt>', re.S)#正则
    tu_1 = ''.join(title_and_url.findall(html))
    # 加换行，并删除字符
    tu_2 = ((((tu_1.replace('</a>','\n'))
              .replace('</font>',''))
             .replace('<font color=#FF0000>',''))
            .replace('  target="_blank">',''))\
        .replace('&nbsp;','')

    #匹配标题
    pattern = re.compile(".*html'(.*)")
    title_list = re.findall(pattern, tu_2)

    #匹配链接
    moe_url = re.compile("[a-zA-z]+://[^\s]*.html?")
    url_list = re.findall(moe_url, tu_2)

    #匹配时间格式
    moe_time = re.compile("\\d{4}-\\d{2}-\\d{2}")
    addtime = re.findall(moe_time, html)

    #调用写入mysql数据库函数
    mysql_write(url_list, title_list, addtime)

    #数据写入txt文件
    # day = datetime.datetime.now().strftime('%Y_%m_%d')  # 读取日期
    #txtfile = open(day + ".txt", 'a', encoding="utf-8")
    #txtfile.write("".join(addtime) + "\n")

while (1):
    request()
    print('完成了第' + str(page) + '页的链接爬取！')
    page = page + 1
    if (test() == ''):
        print('爬取结束！！')
        break;

