from bs4 import BeautifulSoup


def article_desc(content):
    soup = BeautifulSoup(content, "html.parser")
    # 文章过滤：
    for tag in soup.find_all():
        if tag.name in ["script", ]:
            tag.decompose()
    # 切片文章文本
    desc = soup.text[0:150]
    return desc
