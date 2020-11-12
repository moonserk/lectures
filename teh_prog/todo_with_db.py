# Подключение библиотек
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq

#Создание основного фрейма
root = tk.Tk()
root.title('Список дел')
root.geometry("400x400")

connection = sq.connect('todo.db') # Подключение к базе данных
cursor = connection.cursor() # Объект для манипулирование базой данных
cursor.execute('create table if not exists tasks (title text)') # Создание таблицы если она не существует

#Инициализация массива для добавления заданий
tasks = []

#Функция добавления задания
def addTask():
    word = input_entry.get()
    if len(word)==0:
        messagebox.showinfo('Отсутствуют данные', 'Введите задачу')
    else:
        tasks.append(word)
        cursor.execute('insert into tasks values (?)', (word,)) # Добавление задачи в таблицу
        listUpdate()
        input_entry.delete(0,'end')

#Функция удаления задания
def delOne():
    try:
        val = list_box.get(list_box.curselection())
        if val in tasks:
            tasks.remove(val)
            listUpdate()
            cursor.execute('delete from tasks where title = ?', (val,)) # Удаление задачи из таблицы
    except:
            messagebox.showinfo('Невозможно удалить', 'Не выбрана задача')

# Функция для инициализации данных из базы данных в программу
def retrieveDB():
        while(len(tasks)!=0):
            tasks.pop()
        for row in cursor.execute('select title from tasks'):
            tasks.append(row[0])

#Фукция обновления листа с заданиями
def listUpdate():
    clearList()
    for i in tasks:
        list_box.insert('end', i)

#Функция очистки списка
def clearList():
    list_box.delete(0,'end')

#Функция выхода из приложения
def bye():
    root.destroy()

#Инициализация UI компонентов
title = ttk.Label(root, text = 'Список дел')
input_label = ttk.Label(root, text='Введите задачу: ')
input_entry = ttk.Entry(root, width=20)
list_box = tk.Listbox(root, height=15, selectmode='SINGLE')
add_btn = ttk.Button(root, text='Добавить', width=20, command=addTask)
del_btn = ttk.Button(root, text='Удалить', width=20, command=delOne)
exit_btn = ttk.Button(root, text='Выход', width=20, command=bye)

retrieveDB()
listUpdate()

input_label.place(x=20, y=40)
input_entry.place(x=20, y=60)
add_btn.place(x=20, y=90)
del_btn.place(x=20, y=120)
exit_btn.place(x=20, y =305)
title.place(x=20, y=10)
list_box.place(x=220, y=60)

#Главный цикл обработки событий
root.mainloop()

connection.commit() # Утверждение изменений в базе данных
cursor.close() # Закрытие соединения с бд
