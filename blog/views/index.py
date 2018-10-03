from flask import Blueprint, render_template, Flask, request, redirect,session
from ..utils import helper
ind = Blueprint('ind', __name__)



@ind.route('/page=<page>')
@ind.route('/',methods=['POST','GET'])
def hello_world(page=None):
    select = request.form.get('select')
    if select:
        data_list = helper.fetch_all("select id,title,des,create_time from article WHERE TITLE LIKE %s", ('%'+select+'%',))


    else:
        data_list = helper.fetch_all('select id,title,des,create_time from article', [])

    category_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2,count(*) as b FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID GROUP BY CATEGORY.id',[])
    month_list = helper.fetch_all("SELECT count(id) as c, DATE_FORMAT(create_time,'%%Y-%%m') as d FROM article GROUP BY DATE_FORMAT(create_time,'%%Y-%%m') desc",[])



    from ..utils.pagination import Pagination
    count = helper.fetch_all('SELECT COUNT(1) FROM article',[])
    total_count = count[0]['COUNT(1)']
    page = Pagination(page, total_count, request.path, per_page=2)
    data_list = data_list[page.start:page.end]

    return render_template('index.html',data_list=data_list,category_list=category_list,month_list=month_list,page=page)



@ind.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = helper.fetch_one('select id from user WHERE username=%s and password=%s',(email,password))
        if user:
            session['user_info'] = {'email':email}
            return redirect('/backend/')
    return render_template('login.html')

@ind.route('/category/<int:nid>/page=<page>')
@ind.route('/category/<int:nid>')
def category(nid,page=None):
    data_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2 FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID WHERE CATEGORY.id=%s', (nid,))

    category_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2,count(*) as b FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID GROUP BY CATEGORY.id',[])
    month_list = helper.fetch_all("SELECT count(id) as c, DATE_FORMAT(create_time,'%%Y-%%m') as d FROM article GROUP BY DATE_FORMAT(create_time,'%%Y-%%m') desc",[])

    from ..utils.pagination import Pagination
    count = helper.fetch_all('SELECT COUNT(1) FROM article', [])
    total_count = count[0]['COUNT(1)']
    page = Pagination(page, total_count, request.path, per_page=10)
    data_list = data_list[page.start:page.end]

    return render_template('index.html',data_list=data_list,category_list=category_list,month_list=month_list,page=page)


@ind.route('/month/<string:month>/page=<page>')
@ind.route('/month/<string:month>')
def month_list(month,page=None):
    month = helper.fetch_all("SELECT id,title,create_time,des FROM article WHERE DATE_FORMAT(create_time,'%%Y-%%m')=%s",(month,))
    category_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2,count(*) as b FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID GROUP BY CATEGORY.id',[])
    month_list = helper.fetch_all("SELECT count(id) as c, DATE_FORMAT(create_time,'%%Y-%%m') as d FROM article GROUP BY DATE_FORMAT(create_time,'%%Y-%%m') desc",[])

    from ..utils.pagination import Pagination
    count = helper.fetch_all('SELECT COUNT(1) FROM article', [])
    total_count = count[0]['COUNT(1)']
    page = Pagination(page, total_count, request.path, per_page=10)
    data_list = month[page.start:page.end]

    return render_template('index.html',data_list=month,category_list=category_list,month_list=month_list,page=page)



@ind.route('/article_detail/<int:nid>')
def article_detail(nid):
    article_obj = helper.fetch_one('SELECT title,content from article WHERE id=%s', (nid,))
    category_list = helper.fetch_all('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.id as nid,CATEGORY.title as title2,count(*) as b FROM (SELECT id,title,create_time,des,content,category_id FROM article) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID GROUP BY CATEGORY.id',[])
    month_list = helper.fetch_all("SELECT count(id) as c, DATE_FORMAT(create_time,'%%Y-%%m') as d FROM article GROUP BY DATE_FORMAT(create_time,'%%Y-%%m') desc",[])

    return render_template('home.html', article_obj=article_obj,category_list=category_list,month_list=month_list)