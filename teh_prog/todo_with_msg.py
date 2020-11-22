# Подключение библиотек
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#Создание основного фрейма
root = tk.Tk()
root.title('Список дел')
root.geometry("500x400")

#Инициализация массива для добавления заданий
tasks = []

#Функция добавления задания
def addTask():
    word = input_entry.get()
    if len(word)==0:
        messagebox.showinfo('Отсутствуют данные', 'Введите задачу')
    else:
        tasks.append(word)
        listUpdate()
        input_entry.delete(0,'end')

#Функция удаления задания
def delOne():
    try:
        val = list_box.get(list_box.curselection())
        if val in tasks:
            tasks.remove(val)
            listUpdate()
    except:
        messagebox.showinfo('Невозможно удалить', 'Не выбрана задача')

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
    answer = messagebox.askyesno(title="Выход", message="Вы действительно хотите выйти?")
    if answer:
        root.destroy()

#Инициализация UI компонентов
title = ttk.Label(root, text = 'Список дел')
input_label = ttk.Label(root, text='Введите задачу: ')
input_entry = ttk.Entry(root, width=20)
list_box = tk.Listbox(root, height=15, selectmode='SINGLE')
add_btn = ttk.Button(root, text='Добавить', width=20, command=addTask)
del_btn = ttk.Button(root, text='Удалить', width=20, command=delOne)
exit_btn = ttk.Button(root, text='Выход', width=20, command=bye)

input_label.place(x=20, y=40)
input_entry.place(x=20, y=60)
add_btn.place(x=20, y=90)
del_btn.place(x=20, y=120)
exit_btn.place(x=20, y =305)
title.place(x=20, y=10)
list_box.place(x=260, y=60)

#Главный цикл обработки событий
root.mainloop()
