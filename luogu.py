import re
import urllib.request
import bs4
import time

base_url = "https://www.luogu.com.cn/problem/P"
save_path = "D:\\Mypython\\newluogu\\"
min_num = 1046
max_num = 1050  # 通过修改起始和终止题号爬取相应的题目


def main():
    print("计划爬取到P{}".format(max_num))
    for i in range(min_num, max_num + 1):
        print("正在爬取P{}...".format(i), end="")
        html = get_html(base_url + str(i))
        if html == "error":
            print("爬取失败，可能是不存在该题或无权查看")
        else:
            problem_md = get_md(html)
            print("爬取成功！正在保存...", end="")
            save_data(problem_md, "P" + str(i) + ".md")
            time.sleep(1)  # 暂停1秒钟
            print("保存成功!")
    print("爬取完毕")


def get_html(url):
    headers = {
        "User-Agent": "Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 85.0.4183.121 Safari / 537.36"
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if "Exception" not in html:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"


def get_md(html):
    bs = bs4.BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md


def save_data(data, filename):
    complete_filename = save_path + filename
    file = open(complete_filename, "w", encoding="utf-8")
    file.write(data)
    file.close()


if __name__ == '__main__':
    main()
