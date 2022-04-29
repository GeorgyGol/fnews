from flask import render_template, request
import app
from app.database.models import NNew

@app.appFL.route('/')
def index():
    nnews = NNew.query.order_by(NNew.NDate.desc())#.limit(10)
    return render_template('news.html')#, nnews=nnews)

@app.appFL.route('/api/data')
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
        if col_name not in ['NDate',]:
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

@app.appFL.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.appFL.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.appFL.run(debug=True)

