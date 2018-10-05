import os
import json
from uuid import uuid4
import markdown
from flask import Blueprint, render_template, Flask, request, redirect,session,jsonify

from settings import Config
from ..utils import helper,article_soup



account = Blueprint('account', __name__)


@account.before_request
def process_request():
    if not session.get('user_info'):
        return redirect("/login/")
    return None


@account.route('/backend/')
def backend():
    data_list = helper.fetch_all('SELECT id,title,create_time FROM article', [])
    return render_template('backend/backend.html',data_list=data_list)


@account.route('/backend/delete_article/',methods=['POST'])
def delect_article():
    data = json.loads(request.get_data())
    del_id = int(data.get('article_id'))
    helper.insert('DELETE FROM article WHERE id=%s',(del_id,))
    return '删除成功'




@account.route('/upload/',methods=['POST','GET'])
def upload():
    obj = request.files.get('editormd-image-file')
    name = str(uuid4())
    path = os.path.join(Config.BASE_DIR,'blog',"static", "upload",name)
    print(path)
    with open(path,'wb') as f:
        for line in obj:
            f.write(line)

    res = {
        'success': 1,
        'message': u'图片上传成功',
        'url': "/static/upload/"+name
    }
    return jsonify(res)


@account.route('/backend/add_article/',methods=['POST','GET'])
def add_article():
    if request.method == 'GET':
        cate_list = helper.fetch_all('SELECT id,title FROM category', [])
        return render_template('backend/add_article.html',cate_list=cate_list)


    title = request.form.get('title')
    content = request.form.get('editormd-html-code')
    content = markdown.markdown(content,extensions=Config.exts)

    cate_id = request.form.get('cate')
    desc = article_soup.article_desc(content)
    helper.insert('INSERT INTO ARTICLE (title,des,content,category_id) VALUE (%s,%s,%s,%s)',(title,desc,content,cate_id))
    return redirect('/backend/')



@account.route('/backend/edit_article/<int:nid>',methods=['POST','GET'])
def edit_article(nid):
    if request.method == "GET":
        article_obj = helper.fetch_one('SELECT A.id,A.title,A.create_time,A.des,A.content,CATEGORY.title as title2 FROM (SELECT id,title,create_time,des,content,category_id FROM article WHERE id=%s) as A LEFT JOIN CATEGORY ON A.category_id=CATEGORY.ID',(nid,))
        cate_list = helper.fetch_all('SELECT id,title FROM category', [])
        return render_template('backend/edit_article.html',article_obj=article_obj,cate_list=cate_list)

    title = request.form.get('title')
    content = request.form.get('editormd-html-code')
    content = markdown.markdown(content,extensions=Config.exts)

    cate_id = request.form.get('cate')
    desc = article_soup.article_desc(content)
    helper.insert('UPDATE article set title=%s,des=%s,content=%s,category_id=%s WHERE id=%s',(title,desc,content,cate_id,nid))
    return redirect('/backend/')


