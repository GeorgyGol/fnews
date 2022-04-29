from enum import Enum
import app

database = app.database #.SQLAlchemy(app.appFL)

class VISIBILITY(Enum):
    YES = -1
    NO = 0

class NNew(database.Model):
    __tablename__ = 'news'

    ID = database.Column(database.Integer, primary_key = True)
    NDate = database.Column(database.DateTime, index = True, unique = False)
    NText = database.Column(database.Text)
    IsVisible = database.Column(database.SmallInteger, default = VISIBILITY.YES)

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


def create_db():
    database.create_all()

def test_news():
    news = NNew.query.order_by(NNew.NDate.desc()).limit(10)

    for n in news:
        print(n)

if __name__ == '__main__':
    test_news()
