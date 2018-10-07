from flask import Blueprint, render_template, Flask, request, redirect,session

from ..utils import helper
from ..utils.pagination import Pagination

ind = Blueprint('ind', __name__)

def select_blog(sql,*args):
    select = request.form.get('select')
    if select:
        data_list = helper.fetch_all("select id,title,des,create_time from article WHERE TITLE LIKE %s order by create_time desc",
                                     ('%'+select+'%',))
    else:
        data_list = helper.fetch_all(sql, (args))
    category_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2,count(1) as b FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID GROUP BY CATEGORY.id',[])
    month_list = helper.fetch_all("SELECT count(id) as c, DATE_FORMAT(create_time,'%%Y-%%m') as d FROM article GROUP BY DATE_FORMAT(create_time,'%%Y-%%m') desc",[])
    return data_list,category_list,month_list,select

def page_html(data_list,select):
    page = int(request.args.get('page',1))
    if select:
        count = helper.fetch_all("select COUNT(1) from article WHERE TITLE LIKE %s",
                                 ('%' + select + '%',))
    else:
        count = helper.fetch_all('SELECT COUNT(1) FROM article',[])
    total_count = count[0]['COUNT(1)']
    page = Pagination(page, total_count, request.path)
    data_list = data_list[page.start:page.end]
    return data_list,page

# @ind.route('/page=<int:page>',methods=['POST','GET'])
@ind.route('/',methods=['POST','GET'])
def index():
    sql = 'select id,title,des,create_time from article order by create_time desc'
    data_list, category_list, month_list,select = select_blog(sql)

    data_list,page = page_html(data_list,select)

    return render_template('index.html',data_list=data_list,category_list=category_list,month_list=month_list,page=page.page_html)



@ind.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = helper.fetch_one('select id from user WHERE username=%s and password=%s',
                                (email,password))
        if user:
            session['user_info'] = {'email':email}
            return redirect('/backend/')
    return render_template('login.html')


# @ind.route('/category/<int:nid>/page=<int:page>',methods=['POST','GET'])
@ind.route('/category/<int:nid>',methods=['POST','GET'])
def category(nid):
    sql = 'SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2 FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID WHERE CATEGORY.id=%s order by create_time desc'
    data_list, category_list, month_list,select = select_blog(sql,nid)

    data_list,page = page_html(data_list, select)

    return render_template('index.html',data_list=data_list,category_list=category_list,month_list=month_list,page=page.page_html)


# @ind.route('/month/<string:month>/page=<int:page>',methods=['POST','GET'])
@ind.route('/month/<string:month>',methods=['POST','GET'])
def month_list(month):

    sql = "SELECT id,title,create_time,des FROM article WHERE DATE_FORMAT(create_time,'%%Y-%%m')=%s order by create_time desc"
    month, category_list, month_list,select = select_blog(sql,month)

    month,page = page_html(month, select)
    return render_template('index.html',data_list=month,category_list=category_list,month_list=month_list,page=page.page_html)


@ind.route('/article_detail/<int:nid>',methods=['POST','GET'])
def article(nid):

    sql = 'select id from article'
    _, category_list, month_list,select = select_blog(sql)
    if select:
        article_obj = helper.fetch_all("select id,title,des,create_time from article WHERE TITLE LIKE %s",
                                     ('%' + select + '%',))
        article_obj,page = page_html(article_obj, select)

        return render_template('index.html', data_list=article_obj, category_list=category_list, month_list=month_list,page=page.page_html)
    else:
        article_obj = helper.fetch_one('SELECT title,create_time,content from article WHERE id=%s', (nid,))
    return render_template('home.html', article_obj=article_obj,category_list=category_list,month_list=month_list)