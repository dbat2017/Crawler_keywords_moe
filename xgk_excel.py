import urllib.request, re, datetime
import xlwt

#默认页码为1
page = 1
id = 1
row = 0
#头文件
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}
data = None

workbook = xlwt.Workbook(encoding='ascii')
sheet1 = workbook.add_sheet('moe_gov_cn', cell_overwrite_ok=True)
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = 'Times New Roman'
font.bold = True  # 黑体
font.underline = True  # 下划线
font.italic = True  # 斜体字
style.font = font
day = datetime.datetime.now().strftime('%Y_%m_%d')
name_date = day + '.xls'


#测试是否为空
def test():
    #http://www.moe.gov.cn/was5/web/search?channelid=255182&searchword=%E6%96%B0%E5%B7%A5%E7%A7%91&andsen=%E6%96%B0%E5%B7%A5%E7%A7%91&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME%2CRELEVANCE&page=2
    searchurl = 'http://www.moe.gov.cn/was5/web/search?channelid=255182&searchword=%E6%96%B0%E5%B7%A5%E7%A7%91&andsen=%E6%96%B0%E5%B7%A5%E7%A7%91&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME%2CRELEVANCE&page=' + str(page)
    req = urllib.request.Request(url = searchurl, data = data, headers = headers, method = 'GET')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    txt = re.compile('<h2><a href=(.*?)</h2></dt>', re.S)
    return (''.join(txt.findall(html)))

#页面代码数据获取，正则匹配,写入excel
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

    #数据写入excel文件
    for t in range(len(title_list)):
        a = t + (page-1)*20
        sheet1.write(a, 0, str(a+1))
        sheet1.write(a, 1, title_list[t])
        sheet1.write(a, 2, url_list[t])
        sheet1.write(a, 3, addtime[t])
        workbook.save(name_date)

while (1):
    request()
    print('完成了第' + str(page) + '页的链接爬取！')
    page = page + 1
    if (test() == ''):
        print('爬取结束！！')
        break;

