# Подключение библиотек
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas
from tkinter import PhotoImage
import sqlite3 as sq

#Создание основного фрейма
root = tk.Tk()
root.title('Список дел')
root.geometry("500x500")

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
    ans = messagebox.askyesno("Выход?", "Вы действительно хотите выйти?")
    if ans:
        root.destroy()




frames = []
for i in range(100):
    try:
        frames.append([PhotoImage(file='spiner.gif',format = 'gif -index %i' %(i))])
    except:
        break

def anim():
    i = 0

    def next_shot():
        nonlocal i
        canvas.create_image(0, 0, anchor='nw', image=frames[i])
        if i < len(frames) - 1:
            i += 1
            root.after(50, next_shot)
        else:
            canvas.destroy()
            canvas2.destroy()

    return next_shot

#Инициализация UI компонентов
title = ttk.Label(root, text = 'Список дел')
input_label = ttk.Label(root, text='Введите задачу: ')
input_entry = ttk.Entry(root, width=20)
list_box = tk.Listbox(root, height=15, selectmode='SINGLE')
add_btn = ttk.Button(root, text='Добавить', width=20, command=addTask)
del_btn = ttk.Button(root, text='Удалить', width=20, command=delOne)
exit_btn = ttk.Button(root, text='Выход', width=20, command=bye)
canvas2 = Canvas(root, width=500, height=500, bg='white', highlightthickness=0)
canvas = Canvas(root, width=320, height=240, bg='white', highlightthickness=0)

retrieveDB()
listUpdate()

canvas.place(relx=0.5, rely=0.5, anchor='center')
canvas2.place(x=0,y=0)
#canvas2.create_rectangle(500, 500, 0, 0, outline='white', fill='white' )

input_label.pack() #place(x=20, y=40)
input_entry.pack() #place(x=20, y=60)
add_btn.pack() #place(x=20, y=90)
del_btn.pack() #place(x=20, y=120)
exit_btn.pack(side='bottom') #place(x=20, y =305)
title.pack() #place(x=20, y=10)
list_box.pack() #place(x=220, y=60)
#canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.5, relheight=0.5)

anim()()
#Главный цикл обработки событий
root.mainloop()

connection.commit() # Утверждение изменений в базе данных
cursor.close() # Закрытие соединения с бд
