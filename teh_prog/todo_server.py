# Подключение библиотек
import sqlite3 as sq
import socket
import pickle


sock = socket.socket()
sock.bind(('', 9078))
sock.listen(1)



connection = sq.connect('todo.db') # Подключение к базе данных
cursor = connection.cursor() # Объект для манипулирование базой данных
cursor.execute('create table if not exists tasks (title text)') # Создание таблицы если она не существует

#Инициализация массива для добавления заданий
tasks = []

# Функция для инициализации данных из базы данных в программу
def retrieveDB():
        while(len(tasks)!=0):
            tasks.pop()
        for row in cursor.execute('select title from tasks'):
            tasks.append(row[0])


retrieveDB()
data = pickle.dumps(tasks)

# print(tasks, tasks[0])

while True:
    conn, addr = sock.accept()
    conn.send(data)
    data = conn.recv(1024)
    if data:
        for row in pickle.loads(data):
            cursor.execute('insert into tasks values (?)', (row,))
    
    conn.close()    


connection.commit() # Утверждение изменений в базе данных
cursor.close() # Закрытие соединения с бд
