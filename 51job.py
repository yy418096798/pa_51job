import requests
from lxml import etree
import time
import xlwt
import os

def main( job, page):
    url = "https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?".format(job, page)
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    tree = etree.HTML(html)
    # print(tree)
    # job_list = tree.xpath('//div[@class="dw_table"]/div[@class="el"]')
    # print(job_list)
    job_names = tree.xpath('//div[@class="dw_table"]/div[@class="el"]/p/span/a/@title')
    job_boss = tree.xpath('//div[@class="dw_table"]/div[@class="el"]/span/a/@title')
    # print(job_boss)
    job_place = tree.xpath('//div[@class="dw_table"]/div[@class="el"]/span[2]/text()')
    job_maney = tree.xpath('//div[@class="dw_table"]/div[@class="el"]/span[3]/text()')
    job_time = tree.xpath('//div[@class="dw_table"]/div[@class="el"]/span[4]/text()')

    # job_list = []
    for name, boss, place, maney, time in zip(job_names, job_boss, job_place, job_maney, job_time):
        dict = {"职位名":name, "公司名":boss, "工作地点":place, "薪资":maney, "发布时间":time}
        job_list.append(dict)


def exl():
    # 写入excel表格
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(job)

    # 样式
    style1 = xlwt.XFStyle()
    font1 = xlwt.Font()
    font1.name = '宋体'
    font1.colour_index = 14
    style1.font = font1
    worksheet.col(0).width = 60*256
    worksheet.col(1).width = 48*256
    worksheet.col(2).width = 20*256
    worksheet.col(3).width = 20*256
    worksheet.col(4).width = 10*256

    # 写入第一行
    title = ["职位名", "公司名", "工作地点", "薪资", "发布时间"]

    for t in range(5):
        worksheet.write(0, t, title[t] , style1)

    # 写每一列
    for j in range(1, len(job_list)):
          # 每一行
        for i in range(5):
            hang = job_list[j]
            worksheet.write(j, i, hang.get(title[i]))

    workbook.save(os.getcwd() +"\\51job.xls")

if __name__ == '__main__':
    try:
        job_list = []
        job = input("请输入你想要的工作：")
        start_page = int(input("请输入开始页码："))
        end_page = int(input("请输入结尾页码："))
        for page in range(start_page, end_page + 1):
            main(job, page)
            print("第"+ str(page) +"获取成功")
            # time.sleep(1)
            if page % 10 == 0 :
                print("每下载10页休息5秒")
                time.sleep(5)

        exl()
        print("下载结束")
    except:
        print("输入格式有误，请重新检查后输入")
