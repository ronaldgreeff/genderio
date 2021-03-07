import os
from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask import Blueprint
from .. import db
from ..models import Pages


main = Blueprint('cms', __name__)


@app.route('/', subdomain='blog')
def index():
    pages = db.session.query(Pages).all()
    return render_template('cms_index.html', pages=pages)


@app.route('/page/<int:page_id>', subdomain='blog')
def view_page(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template(
        'page.html', id=page.id,
        title=page.title, content=page.content)


@app.route('/edit-page/<int:page_id>', subdomain='blog')
def edit_page(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('edit-page.html',
                           id=page.id, title=page.title, content=page.content)


@app.route('/update-page/', subdomain='blog', methods=['POST'])
def update_page():
    page_id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    db.session.query(Pages).filter_by(id=page_id).update({'title': title,
                                                          'content': content})
    db.session.commit()
    return redirect('/page/'+page_id)


@app.route('/new-page/', subdomain='blog')
def new_page():
    return render_template('new-page.html')


@app.route('/save-page/', subdomain='blog', methods=['POST'])
def save_page():
    page = Pages(title=request.form['title'],
                 content=request.form['content'])
    db.session.add(page)
    db.session.commit()
    return redirect('/page/%d' % page.id)


@app.route('/delete-page/<int:page_id>', subdomain='blog')
def delete_page(page_id):
    db.session.query(Pages).filter_by(id=page_id).delete()
    db.session.commit()
    return redirect('/')
