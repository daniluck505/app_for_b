import pywebio
from pywebio import input
from pywebio import output
import pandas as pd
from pywebio.session import defer_call, info as session_info, run_async, run_js

df_printer = pd.read_csv('df_printer.csv')
df_person = pd.read_csv('df_person.csv')


def saver_df_person(df_data, name, exel=False):
    """Функция сохранения датафрейма в файл"""
    if exel:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_excel(name + 'xlsx' + '.xlsx')
    else:
        df_data[['nickname', 'name', 'surname', 'parol', 'status', 'work_time']].to_csv(name + '.csv')


def saver_df_printer(df_data, name, exel=False):
    """Функция сохранения датафрейма в файл"""
    if exel:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_excel(name + 'xlsx' + '.xlsx')
    else:
        df_data[['number', 'name', 'profit', 'work_time', 'description', 'chat', 'status']].to_csv(name + '.csv')


def reset_df_person():
    df_person = pd.DataFrame(columns=['nickname', 'name', 'surname', 'parol', 'status', 'work_time'])
    saver_df_person(df_person, 'df_person')


def reset_df_printer():
    df_printer = pd.DataFrame(columns=['name', 'profit', 'work_time', 'description', 'chat'])
    saver_df_printer(df_printer, 'df_printer')

reset_df_person()

print(df_person)
