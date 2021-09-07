from flask import render_template, redirect, url_for, flash
from app.auth.views import login_required
from app.dao.websites_dao.iwebsitesdao import IWebsitesdao
from app.dao.websites_dao.websitesdaoimp import Websitedao
from app.websites import Website
from . import main
from .forms import AddAccount, EditWeb


@main.route('/')
@login_required
def index():
    form = AddAccount()
    website = Website(form)
    websitedao: IWebsitesdao
    websitedao = Websitedao()
    webs = websitedao.get_all(website.user_id)
    return render_template('index.html', webs=webs)


@main.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    form = AddAccount()
    websitedao: IWebsitesdao

    if form.validate_on_submit():
        website = Website(form)
        websitedao = Websitedao()
        websitedao.add(website)
        flash('Perfil Guardado correctamente')
    return render_template('add_account.html', form=form)


@main.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    websitedao: IWebsitesdao()
    websitedao = Websitedao()
    web = websitedao.get(id)
    form = EditWeb(username=web['web_username'], url=web['web_name'], password=web['web_pass'], notas=web['nota'], email=web['web_email'])
    return render_template('update_webs.html', web=web, form=form)


@main.route('/update/<string:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    web_form = EditWeb()
    website = Website(web_form)
    websitedao: IWebsitesdao
    websitedao = Websitedao()
    websitedao.update(website, id)
    flash('Datos actualizados')
    return redirect(url_for('main.index'))


@main.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    form = AddAccount()
    website = Website(form)
    websitedao: IWebsitesdao
    websitedao = Websitedao()
    websitedao.delete(id)
    flash('Dato Eliminado correctamente')
    return redirect(url_for('main.index'))
