from enum import Enum
import app
import datetime as dt

db_main = app.db_main #.SQLAlchemy(app.appFL)

class VISIBILITY(Enum):
    YES = -1
    NO = 0

class NNew(db_main.Model):
    __tablename__ = 'news'

    ID = db_main.Column(db_main.Integer, primary_key = True)
    NDate = db_main.Column(db_main.DateTime, index = True, unique = False)
    NText = db_main.Column(db_main.Text)
    IsVisible = db_main.Column(db_main.SmallInteger, default = VISIBILITY.YES)

    def __repr__(self):
        return f'# {self.ID}; {self.NDate.strftime("%Y-%m-%d")}; {self.NText} - vis={self.IsVisible}'

    def to_dict(self):
        _d = {
            'ID':self.ID,
            'NDate':self.NDate.strftime('%Y-%m-%d<br>%H:%M'),
            'NText':self.NText,
            'IsVisible':self.IsVisible
        }
        return _d


def update_db(nnum=None, ndate=None, ntext='', isVis=True):
    assert nnum
    assert type(ndate==dt.datetime)

    try:
        nnum = int(nnum)
        newnew = NNew.query.filter_by(ID=nnum).update(dict(NText=ntext, NDate=ndate, IsVisible=isVis))
    except ValueError:
        newnew = NNew(NDate = ndate, NText = ntext, IsVisible = isVis)
        db_main.session.add(newnew)
    db_main.session.commit()
    try:
        db_main.session.refresh(newnew)
        return newnew.ID
    except:
        return nnum


def delete_new(nnum):
    assert nnum
    try:
        nnum = int(nnum)
    except:
        raise ValueError('Нельзя удалить то, чего нет')

    deleted = NNew.query.filter_by(ID=nnum).first()
    db_main.session.delete(deleted)
    db_main.session.commit()


def create_db():
    db_main.create_all()

def test_news():
    news = NNew.query.order_by(NNew.NDate.desc()).limit(10)

    for n in news:
        print(n)

if __name__ == '__main__':
    # test_news()
    strD = '2022-04-26 16:03:00'
    strT = '''Подготовлено исследование !!! <a href = "http://www.forecast.ru/_ARCHIVE/Analitics/Soln/BSVAR1.pdf">"Оценка ффективности мер денежно-кредитной политики и валютного контроля в условиях санкционного давления на российскую экономику"</a><br><i>В данном исследовании анализируются макроэкономические последствия применения инструментов денежно - кредитной политики и валютного контроля в условиях санкций. Используя модель байесовской структурной векторной авторегрессии(BSVAR), мы показываем, что контроль над движением потоков капитала является весьма эффективной
мерой антикризисного регулирования. Он позволяет поддержать объемы экспорта и импорта, сохранить уверенную динамику
    корпоративного кредитования и, при этом, не оказывает дестабилизирующего воздействия на курс рубля и инфляцию. </i>'''
    isV = True
    print(dt.datetime.now())
    # print(update_db(nnum='3301', ntext='texting str', ndate=dt.datetime.now(), isVis=False))
    delete_new('3301')
