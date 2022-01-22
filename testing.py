import pywebio
from pywebio import input
from pywebio import output
import pandas as pd
import asyncio
from pywebio.session import defer_call, info as session_info, run_async, run_js

# --------------------Добавляем файлы----------------
df_printer = pd.read_csv('df_printer.csv')
df_person = pd.read_csv('df_person.csv')
print(df_person)
print(df_printer)


# -------------------Функции----------------
def saver_df_person(df_data, name, exel=False):
    """Функция сохранения датафрейма в файл"""
    if exel:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_excel(name + 'xlsx' + '.xlsx')
    else:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_csv(name + '.csv')


def saver_df_printer(df_data, name, exel=False):
    """Функция сохранения датафрейма в файл"""
    if exel:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_excel(
            name + 'xlsx' + '.xlsx')
    else:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_csv(name + '.csv')


def append_df_person():
    """Функция добалвения нового пользователя"""
    control_regist = True
    try:
        while control_regist:
            output.clear()
            global df_person
            data_regist = input.input_group("Регистрация", [
                input.input('Введите nickname', name='nickname'),
                input.input('Введите имя', name='name'),
                input.input('Введите фамилию', name='surname'),
                input.select('Выберите должность', ['Руководитель', 'Курьер', 'Мастер'], name='status'),
                input.input('Введите пароль', name='password_1', type='password'),
                input.input('Повторите пароль', name='password_2', type='password')
            ])
            nickname_prov, password_prov = False, False
            if data_regist['nickname'] not in list(df_person['nickname']):
                nickname_prov = True
            else:
                output.put_markdown('## Такой nickname уже существует!')

            if data_regist['password_1'] == data_regist['password_2']:
                password_prov = True
            else:
                output.put_markdown('## Пароль не совпал!')
            if nickname_prov == True and password_prov == True:
                # Создаем нового пользователя
                new_row = {'nickname': data_regist['nickname'],
                           'name': data_regist['name'],
                           'surname': data_regist['surname'],
                           'parol': data_regist['password_1'],
                           'status': data_regist['status'],
                           'work_time': 0}
                df_person = df_person.append(new_row, ignore_index=True)
                output.put_markdown('# Регистрация прошла успешно!')
                control_regist = False
            else:
                output.put_markdown('# Регистрация не удалась')
    except:
        output.put_markdown('# В регистрации прошла ошибка')
        append_df_person()


def control_person_in_df(nickname, password):
    try:
        if str(df_person[df_person['nickname'] == nickname]['parol'][0]) == str(password):
            return True
        else:
            print('трабл')
            return False
    except:
        print('Ошибка')
        return False


def aoutor():
    """Функция авторизации"""
    autoriz = True
    while autoriz:
        output.clear()
        output.put_markdown('## Авторизация')
        data_basic_info = input.input_group("Вход", [
            input.input('Введите nickname', name='nickname'),
            input.input('Введите пароль', name='password', type='password')
        ])
        # Делаем проверку на присутствие в базе
        password_control = control_person_in_df(data_basic_info['nickname'], data_basic_info['password'])
        print(password_control)
        if password_control:
            output.put_markdown('### Авторизации прошла успешно!')
            autoriz = False
        else:
            output.put_markdown('### Кажется вы не зарегистрированны')
            # output.put_buttons(['Регистрация', 'Назад'], onclick=btn_click_regitr)
            regist = input.select('Выберите пункт', ['Регистрация', 'Назад'])

            if regist == 'Регистрация':
                output.put_markdown('## Регистрация')
                append_df_person()
                autoriz = False


def work_with_df_printer():
    global df_printer
    output.put_markdown('### Меню заказов')
    printer_menu = input.select('Выберите пункт', ['Новый', 'Удалить', 'Изменить', 'Обновить'])

    if printer_menu == 'Новый':
        output.clear()
        data_new_printer = input.input_group("Новый заказ", [
            input.input('Введите имя заказа', name='name'),
            input.input('Введите номер заказа', name='number'),
            input.input('Введите описание заказа', name='description'),

        ])
        new_row = {'name': data_new_printer['name'],
                   'number': data_new_printer['number'],
                   'profit': 0,
                   'work_time': 0,
                   'description': data_new_printer['description'],
                   'status': 'Ожидание'}
        df_printer = df_printer.append(new_row, ignore_index=True)
        saver_df_printer(df_printer, 'df_printer')
    # elif printer_menu == 'Удалить':
    # elif printer_menu == 'Удалить':
    # elif printer_menu == 'Обновить':


def work_with_df_printer_b(action):
    global df_printer
    if action == 'Новый':

        data_new_printer = input.input_group("Новый заказ", [
            input.input('Введите имя заказа', name='name'),
            input.input('Введите номер заказа', name='number'),
            input.input('Введите описание заказа', name='description'),

        ])
        new_row = {'name': data_new_printer['name'],
                   'number': data_new_printer['number'],
                   'profit': 0,
                   'work_time': 0,
                   'description': data_new_printer['description'],
                   'status': 'Ожидание'}
        df_printer = df_printer.append(new_row, ignore_index=True)
        saver_df_printer(df_printer, 'df_printer')

    elif action == 'Удалить':
        pass
    elif action == 'Изменить':
        pass
    elif action == 'Обновить':
        pass

    # elif printer_menu == 'Удалить':
    # elif printer_menu == 'Удалить':
    # elif printer_menu == 'Обновить':


def main_body(status='Руководитель'):
    global df_printer
    with output.put_collapse('Меню'):
        output.put_row([
            output.put_column([
                output.put_button("Новый заказ", onclick=lambda: output.toast("Clicked")),
                output.put_button("Обновить страницу", onclick=lambda btn: run_js('window.location.reload()'))
            ]),
            output.put_column([
                output.put_button("Удалить заказ", onclick=lambda: output.toast("Clicked")),
                output.put_button("Изменить заказ", onclick=lambda: output.toast("Clicked"))
            ]),
            output.put_column([
                output.put_button("Профиль", onclick=lambda: output.toast("Clicked")),
                output.put_button("Настройки", onclick=lambda: output.toast("Clicked"))
            ]),

        ])
    for i in df_printer.index:
        printer_name = df_printer.iloc[i]['name']
        description = df_printer.iloc[i]['description']
        number = df_printer.iloc[i]['number']
        status = df_printer.iloc[i]['status']
        work_time = df_printer.iloc[i]['work_time']

        with output.put_collapse(printer_name):
            output.put_text(description)

            output.put_row([
                output.put_code('Чат'), None,
                output.put_column([
                    output.put_code('Номер: ' + str(number)),
                    output.put_code('Cтатус: ' + str(status)),
                    output.put_code('Общее время работы: ' + str(work_time)),
                    output.put_row([
                        output.put_button('Взять', onclick=output.put_text('lol')), None,
                        output.put_button('Done', onclick=output.put_text('lol')),
                    ])
                ])
            ])


def btn_click(btn_val):
    output.put_text("You click %s button" % btn_val)

def main():
    pywebio.output.put_button('aaaa',onclick=btn_click, position=-1)


if __name__ == '__main__':
    pywebio.start_server(main, debug=True, port=8090, cdn=False)
