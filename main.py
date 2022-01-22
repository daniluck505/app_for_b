import pywebio
from pywebio import input
from pywebio import output
import pandas as pd
import asyncio  # https://docs.python.org/3/library/asyncio.html
from functools import partial

from pywebio.session import defer_call, info as session_info, run_async, run_js

'''
- разобраться с кнопками в главном меню 
- обновление страницы без повторной авторизации 
- загрузка выгрузка файлов ексель для обработки 
- вывод графика статисктики работы 
- чат - как это? нужно встроить 
- настроить гит 
- токен для регистрации 
- надо узнать как делать обновление не всей страницы а отдельных элементов 
'''

# --------------------Добавляем файлы----------------
df_printer = pd.read_csv('df_printer.csv')
df_person = pd.read_csv('df_person.csv')
print(df_person)
print(df_printer)


# -------------------Функции----------------


async def saver_df_person(df_data, name, exel=False):
    """Функция сохранения датафрейма df_person в файл"""
    if exel:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_excel(name + 'xlsx' + '.xlsx')
    else:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_csv(name + '.csv')


async def refresh_person():
    """Функция обновления датафрейма df_person"""
    global df_person
    df_person = pd.read_csv('df_person.csv')


async def saver_df_printer(df_data, name, exel=False):
    """Функция сохранения датафрейма df_printer в файл"""
    if exel:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_excel(
            name + 'xlsx' + '.xlsx')
    else:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_csv(name + '.csv')


async def refresh_printer():
    """Функция обновления датафрейма df_printer"""
    global df_printer
    df_printer = pd.read_csv('df_printer.csv')

"проверка"
async def append_df_person():
    """Функция добалвения нового пользователя"""
    global profile  # global - подгрузка переменной
    global df_person
    control_regist = True
    try:
        while control_regist:
            output.clear()
            data_regist = await input.input_group("Регистрация", [
                await input.input('Введите nickname', name='nickname'),
                await input.input('Введите имя', name='name'),
                await input.input('Введите фамилию', name='surname'),
                await input.select('Выберите должность', ['Руководитель', 'Курьер', 'Мастер', 'Менеджер'],
                                   name='status'),
                await input.input('Введите пароль', name='password_1', type='password'),
                await input.input('Повторите пароль', name='password_2', type='password')
            ])
            nickname_prov, password_prov = False, False

            if data_regist['nickname'] not in list(df_person['nickname']):
                nickname_prov = True
            else:
                output.toast('Такой nickname уже существует!')

            if data_regist['password_1'] == data_regist['password_2']:
                password_prov = True
            else:
                output.toast('Пароль не совпал!')
            if nickname_prov == True and password_prov == True:
                # Создаем нового пользователя
                new_row = {'nickname': data_regist['nickname'],
                           'name': data_regist['name'],
                           'surname': data_regist['surname'],
                           'parol': str(data_regist['password_1']),
                           'status': data_regist['status'],
                           'work_time': 0}
                df_person = df_person.append(new_row, ignore_index=True)
                output.toast('Регистрация прошла успешно!')
                profile = df_person[df_person['nickname'] == data_regist['nickname']]
                await saver_df_person(df_person, 'df_person')
                control_regist = False
            else:
                output.toast('Регистрация не удалась')
    except:
        output.put_markdown('# В регистрации прошла ошибка')
        await append_df_person()


async def control_person_in_df(nickname, password):
    try:
        if nickname in list(df_person['nickname']):
            if str(list(df_person[df_person['nickname'] == nickname]['parol'])[0]) == str(password):
                return True
            else:
                output.toast('Пароль не совпал')
                return False
    except:
        print('Ошибка в проверке пароля')


async def aoutor():
    """Функция авторизации"""
    global profile
    global df_person
    autoriz = True
    while autoriz:
        output.clear()
        output.put_markdown('## Авторизация')
        data_basic_info = await input.input_group("Вход", [
            await input.input('Введите nickname', name='nickname'),
            await input.input('Введите пароль', name='password', type='password')
        ])
        # Делаем проверку на присутствие в базе
        password_control = await control_person_in_df(data_basic_info['nickname'], data_basic_info['password'])
        print(password_control)
        if password_control:
            profile = df_person[df_person['nickname'] == data_basic_info['nickname']]
            autoriz = False
        else:
            output.put_markdown('### Кажется вы не зарегистрированны')
            # output.put_buttons(['Регистрация', 'Назад'], onclick=btn_click_regitr)
            regist = await input.select('Выберите пункт', ['Регистрация', 'Назад'])

            if regist == 'Регистрация':
                output.put_markdown('## Регистрация')
                await append_df_person()
                autoriz = False


async def work_with_df_printer(action, id=False):
    global df_printer
    # output.toast("You click %s button with id: %s" % (action, id))
    if action == 'Новый':
        data_new_printer = await input.input_group("Новый заказ", [
            await input.input('Введите имя заказа', name='name'),
            await input.input('Введите номер заказа', name='number'),
            await input.textarea('Введите описание заказа', name='description'),

        ])
        new_row = {'name': data_new_printer['name'],
                   'number': data_new_printer['number'],
                   'profit': 0,
                   'work_time': 0,
                   'description': data_new_printer['description'],
                   'status': 'Ожидание'}
        if data_new_printer['name'] != None:
            df_printer = df_printer.append(new_row, ignore_index=True)
            await saver_df_printer(df_printer, 'df_printer')
    elif action == 'Удалить':

        print(action, id)
        df_printer = df_printer.drop(id, axis=0)
        print(df_printer.shape[0])
        await saver_df_printer(df_printer, 'df_printer')
    elif action == 'Изменить':
        pass
    elif action == 'Обновить':
        pass


async def main_body():
    global df_printer
    global profile
    # записываем информацию о работнике
    nickname_profile = list(profile['nickname'])[0]
    name_profile = list(profile['name'])[0]
    surname_profile = list(profile['surname'])[0]
    status_profile = list(profile['status'])[0]
    # вывод меню
    output.put_row([
        output.put_column([
            output.put_table([
                ['Профиль', ' '],
                ['nickname', nickname_profile],
                ['Имя', name_profile],
                ['Фамилия', surname_profile],
                ['Должность', status_profile],
            ])
        ]),
        output.put_column([
            output.put_button("Новый заказ",
                              onclick=lambda: work_with_df_printer(action='Новый'),
                              color='primary'),
            output.put_button("Изменить профиль",
                              onclick=lambda: print('nine'),
                              color='primary'),
            output.put_button("Настройки",
                              onclick=lambda: output.toast("Clicked"),
                              color='primary'),
        ])
    ])

    refresh = 0
    while True:
        # спим 1 секунду
        await asyncio.sleep(1)
        # проверяем новые заказы
        await refresh_printer()
        if refresh != df_printer.shape[0]:
            print('Список принтеров изменен')
            output.clear()
            # вывод меню
            output.put_row([
                output.put_column([
                    output.put_table([
                        ['Профиль', ' '],
                        ['nickname', nickname_profile],
                        ['Имя', name_profile],
                        ['Фамилия', surname_profile],
                        ['Должность', status_profile],
                    ])
                ]),
                output.put_column([
                    output.put_button("Новый заказ",
                                      onclick=lambda: work_with_df_printer(action='Новый'),
                                      color='primary'),
                    output.put_button("Изменить профиль",
                                      onclick=lambda: print('nine'),
                                      color='primary'),
                    output.put_button("Настройки",
                                      onclick=lambda: output.toast("Clicked"),
                                      color='primary'),
                ])
            ])

            # вывод заказов
            # можно использовать def
            # можно нафти на что ссылается i в данный момент
            # разобраться с onclick
            for i in df_printer.sort_index(ascending=False).index:
                printer_name = df_printer.iloc[i]['name']
                description = df_printer.iloc[i]['description']
                number = df_printer.iloc[i]['number']
                status = df_printer.iloc[i]['status']
                work_time = df_printer.iloc[i]['work_time']

                print(i)
                with output.put_collapse(printer_name):
                    output.put_text(description)

                    output.put_row([
                        output.put_column([
                            output.put_code('Номер: \n' + str(number)),
                            output.put_code('Cтатус: \n' + str(status)),
                            output.put_code('Общее время работы: \n' + str(work_time)),
                        ]), None,
                        output.put_column([
                            output.put_buttons(['Взять'],
                                               onclick=partial(work_with_df_printer, id=i),
                                               small=True),
                            output.put_buttons(['Готово'],
                                               onclick=partial(work_with_df_printer, id=i),
                                               small=True),
                            output.put_buttons(['Изменить'],
                                               onclick=partial(work_with_df_printer, id=i),
                                               small=True),
                            output.put_buttons(['Архивировать'],
                                               onclick=partial(work_with_df_printer, id=i),
                                               small=True),
                            output.put_buttons(['Удалить'],
                                               onclick=partial(work_with_df_printer, id=i),
                                               small=True),
                        ]),
                    ])
                    output.put_code('Чат'), None,
        # обновляем количество заказов
        refresh = df_printer.shape[0]



# work_with_df_printer(action='Удалить', name=printer_name)

async def main():
    try:
        profile = None
        await aoutor()
        output.clear()
        await main_body()
    except:
        output.put_markdown('# Произошла неизвестная ошибка, попробуйте перезагрузить сайт')
        # журанл ошибок


if __name__ == '__main__':
    pywebio.start_server(main, debug=True, port=8070, cdn=False)
