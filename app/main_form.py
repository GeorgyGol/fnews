from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, InputRequired, length, ValidationError, Regexp
from wtforms.widgets import TextArea, DateTimeInput
import datetime as dt
from bs4 import BeautifulSoup as soup

DATE_FORMAT = '%Y-%m-%d %H:%M'

def date_format_validate(form, field):
    if type(field.data) != dt.datetime:
        print('!'*50)
        raise ValidationError(f'Не правильно дата введена: {field.data}')
    # try:
    #     dt.datetime.strptime(field.data, DATE_FORMAT)
    # except ValueError as err:
    #     raise ValidationError(f'Не правильно дата введена: {err}')
    # return True

def html_validate(strINP):
    sp = soup(strINP, 'html.parser')
    print(sp.get_text())

    return True

class NewsForm(FlaskForm):
    nnum = StringField('Номер:', render_kw={'readonly': True}, default='NEW')
    ndate = DateTimeField('Дата:', validators=[DataRequired()], widget=DateTimeInput(),
                      format=DATE_FORMAT, default=dt.datetime.now())
    ntext = TextAreaField('Текст новости:', validators=[DataRequired()], widget=TextArea())
    isVis = BooleanField('Видимость:', default=True)
    isRSS = BooleanField('to RSS:', default=True)
    isTG = BooleanField('to Telegram:', default=True)
    submit = SubmitField('Сохранить', name='save')
    delete = SubmitField('Удалить', name='delete')




if __name__ == '__main__':
    # print(date_format_validate('2022-05-18'))

    strT = '''Подготовлено исследование <a href="http://www.forecast.ru/_ARCHIVE/Analitics/Soln/BSVAR1.pdf">"Оценка эффективности мер денежно-кредитной политики и валютного контроля в условиях санкционного давления на российскую экономику"<br><i>
В данном исследовании анализируются макроэкономические последствия применения инструментов денежно-кредитной политики и валютного контроля в условиях санкций. Используя модель байесовской структурной векторной авторегрессии (BSVAR), мы показываем, что контроль над движением потоков капитала является весьма эффективной мерой антикризисного регулирования. Он позволяет поддержать объемы экспорта и импорта, сохранить уверенную динамику корпоративного кредитования и, при этом, не оказывает дестабилизирующего воздействия на курс рубля и инфляцию.</i>
    '''
    print(html_validate(strT))