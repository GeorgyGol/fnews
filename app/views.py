from pathlib import Path
from flask import render_template, request, session, redirect, url_for, flash, send_file

from app import app
from app import work_path, user
from app.database.models import NNew, update_db, delete_new
from app.main_form import NewsForm
from app.rss import delete_item, update_rss
from app.telega import send_message2
import time
import datetime as dt

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewsForm()
    form.ndate.data=dt.datetime.now()
    if user == 'DEV':
        work_status = 'dev-settings: local DB and testing telegram'
    else:
        work_status = ''

    # nnews = NNew.query.order_by(NNew.NDate.desc())#.limit(10)
    if request.method == 'POST':
        if 'save' in request.form:
            time.sleep(1)
            if form.validate_on_submit():
                session.pop('DELETE_NEWS', None)
                num = form.nnum.data
                text = form.ntext.data
                dat = form.ndate.data
                isV = form.isVis.data
                isRSS = form.isRSS.data
                isTG = form.isTG.data

                new_id = update_db(nnum=num, ntext=text, ndate=dat, isVis=isV)
                if isRSS:
                    update_rss(ndate=dat, ntext=text, nnum=new_id,
                               file_path=str(Path(work_path, 'rss', 'rss.xml')))

                if isTG and (num == 'NEW'):  # в телеграм - только новые, потому что не умею редактировать
                    send_message2(text)
                flash('Изменения сохранены', 'success')
                if num == 'NEW':
                    return redirect(url_for('index'))
            else:
                flash('Проверь формат даты', 'warning')
        elif 'delete' in request.form:
            num = form.nnum.data
            if num == 'NEW':
                flash('Нельзя удалить то, чего нет', 'info')
                session.pop('DELETE_NEWS', None)
            else:
                strDelAlarm = f'Удаляем новость с номером {num} - если да, еще раз нажать Удалить'
                if 'DELETE_NEWS' in session:
                    session.pop('DELETE_NEWS', None)
                    delete_new(num)
                    try:
                        delete_item(guid=num,
                                    file_path=str(Path(work_path, 'rss', 'rss.xml')))
                    except:
                        pass
                    return redirect(url_for('index'))
                else:
                    flash(strDelAlarm, 'danger')
                    session['DELETE_NEWS'] = strDelAlarm

                # try:
                #     print(session)
                #     if session['DELETE_NEWS'] == strDelAlarm:
                #         print('!'*100)
                #         session['DELETE_NEWS']=''
                #         delete_new(nnum=num)
                #         return redirect(url_for('index'))
                # except:
                #     flash(strDelAlarm, 'danger')
                #     session['DELETE_NEWS'] = strDelAlarm

                # return redirect(url_for('index'))

    else:
        # session.clear()
        session.pop('DELETE_NEWS', None)
    return render_template('news.html', form=form, work_status=work_status,
                           rss_file_path=str(Path(work_path, 'rss', 'rss.xml')))  # , nnews=nnews)


@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = str(Path(work_path, 'rss', 'rss.xml'))
    return send_file(path, as_attachment=True)

@app.route('/api/data')
def data():
    # return {'data': [nnew.to_dict() for nnew in m.NNew.query.order_by(m.NNew.NDate.desc())]}
    query = NNew.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(NNew.NText.like(f'%{search}%'))
    total_filtered = query.count()

    # sorting
    order = []

    i = 0
    # query = query.order_by(m.NNew.NDate.desc())
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break

        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['NDate', ]:
            col_name = 'NDate'
            # descending=True
        else:
            descending = request.args.get(f'order[{i}][dir]') == 'desc'

        col = getattr(NNew, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [nnew.to_dict() for nnew in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': NNew.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # print_env()
    app.run(debug=False, port=5002)
