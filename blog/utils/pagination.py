class Pagination:

    def __init__(self, page_num, total_num, base_url, per_page_num=10, max_show=7):
        self.page_num = page_num
        self.total_num = total_num
        self.base_url = base_url
        self.per_page_num = per_page_num
        self.max_show = max_show
        self.half_show = self.max_show // 2
        self.total_page, more = divmod(total_num, per_page_num)
        if more:
            self.total_page += 1
            if self.total_page < 11:
                self.max_show = self.total_page
        if self.page_num > self.total_page:
            self.page_num = self.total_page
        elif self.page_num < 1:
            self.page_num = 1

    @property
    def start(self):
        return (self.page_num - 1) * self.per_page_num

    @property
    def end(self):
        return self.page_num * self.per_page_num

    @property
    def page_html(self):
        page_start = self.page_num - self.half_show
        page_end = self.page_num + self.half_show + 1
        if self.page_num + self.half_show >= self.total_page:
            page_end = self.total_page + 1
            page_start = self.total_page - self.max_show + 1
        if self.page_num <= self.half_show:
            page_start = 1
            page_end = self.max_show + 1

        page_num_list = []

        # 添加首页
        # page_num_list.append('<li><a href="?page={0}">首页</a></li>'.format(1))
        # 添加上一页
        pre_page_num = self.page_num - 1
        if pre_page_num < 1:
            page_num_list.append(
                '<li style="pointer-events:none"><a href="?page={0}">上一页</a></li>'.format(pre_page_num))
        else:

            page_num_list.append('<li><a href="{0}?page={1}">上一页</a></li>'.format(self.base_url, pre_page_num))

        for i in range(page_start, page_end):

            if i == self.page_num:
                page_num_list.append('<li class="active"><a href="{0}?page={1}" style="color:blue">{2}</a></li>'.format(self.base_url, i, i))
            else:
                page_num_list.append('<li><a href="{0}?page={1}">{2}</a></li>'.format(self.base_url, i, i))
        # 添加下一页
        next_page_num = self.page_num + 1
        if next_page_num > self.total_page:
            page_num_list.append(
                '<li style="pointer-events:none"><a href="?page={0}">下一页</a></li>'.format(next_page_num))
        else:

            page_num_list.append('<li><a href="{0}?page={1}">下一页</a></li>'.format(self.base_url, next_page_num))

        # 添加尾页
        # page_num_list.append('<li><a href="?page={0}">尾页</a></li>'.format(self.total_page))

        page_html = ''.join(page_num_list)

        return page_html
