# Грокаем KEGE с помощью Python.
Библиотека **kegepy** предназначена для работы с сервисом [kompege.ru](https://kompege.ru) (КЕГЭ). С ее помощью вы сможете легко получить данные того или иного задания и варианта. Либа предоставляет возможность получать объект файлов без прямого скачивания на компьютер, получение изображений, ответов и т.д.

- [Классы](#classes)
  - [KEGE](#kege)
  - [Task](#task)
  - [Variant](#variant)
- [Начало работы](#firstWork)
  - [Открытие файлов](#openFiles)
  - [Открытие изображений](#openImages)

# [Классы](#classes)
Ниже описаны основные классы библиотеки.
## [KEGE](#kege)
```python
class KEGE:
    def __init__(self, headers: dict = HEADERS_DEFAULT):
        self.headers = headers
```
- `headers`: (необязательный параметр).
### .search()
`KEGE.search(taskId : int = 0, variantId : int = 0, number_task : int = 0)`  
- `taskId`: айди задания (номер задания).   
- `variantId`: айди варианта (номер кима).   
- `number_task`: номер типа задания из кима.

Метод возвращает в зависимости от входных параметров классы `Task` или `Variant`. Для получения класса `Task` необходимо передать `taskId` или `variantId` с `number_task`. В случае с классом `Variant` передается `variantId`.
## [Task](#task)
```python
class Task:
    id: str
    number: int
    taskId: int
    comment: str
    text: str
    key: str
    hide: bool
    videotype: str
    video: str
    timecode: str
    solve_text: str
    user_id: str
    files: list
    subTask: list
    table: dict
    difficulty: int
    createdAt: str
    updatedAt: str
```
### .get_files_names()
`Task(**kwargs).get_files_names()`  
Метод возвращает список из словарей, имеющие такие ключи:  
- `url`: имя файла на сервере kompege.
- `name`: имя файла при скачивании.
### .open_file()
`Task(**kwargs).open_file(file_number: int = 1, printed: bool = 0, check_access : bool = 0)`  
- `file_number`: порядковый номер файла, который будет открыт.   
- `printed`: показывать дополнительную информацию о файле после открытия.
- `check_access`: запрашивать разрешение на открытие файла.

Метод возвращает класс `TextIOWrapper`. Если файл на сервере имеет формат не .txt, то он автоматически конвертируется в формат .txt. Поддерживаются форматы ``.txt``, ``.xls``, ``.xlsx`` и ``.ods``.
### .open_example()
`Task(**kwargs).open_example()`  
Метод возвращает класс `TextIOWrapper`. Используется для извлечения типового примера из заданий типа 26.  
### .open_image()
`Task(**kwargs).open_image()`  
Метод открывает изображение, прикрепленное к заданию. Поддерживаются форматы ``.png``, ``.jpg`` и ``.gif``.
## [Variant](#variant)
```python
class Variant:
    id: str
    kim: int
    user_id: str
    description: str
    hideAnswer: bool
    oneAttempt: bool
    authRequired: bool
    realMode: bool
    group: str
    type: str
    createdAt: str
    updatedAt: str
    tasks: list
```
### .get_task()
`Variant(**kwargs).get_task(number : int)`  
- `number`: номер типа задания из варианта.

Метод возвращает класс `Task`.
### .get_answers()
`Variant(**kwargs).get_answers()`  
Метод возращает список из словарей, содержащих следующие ключи:  
- `answer`: ответ на задание.
- `taskId`: айди задания.
- `score`: максимальное количество баллов за выполнение задания.
- `number`: номер типа задания.

# [Начало работы](#firstWork)
Для использования необходимо установить следующие либы (версии выше поддерживаются):
```
pillow==11.1.0
pandas==2.1.4
requests==2.31.0
urllib3==2.1.0
```
Для получения объекта задания `Task` или варианта `Variant` необходимо знать их айди (номера). Айди варианта является номером кима, например `2832503195017`. Айди задания можно узнать в базе заданий КЕГЭ, например `2653`.  
```python
from kegepy import KEGE

kege = KEGE()

task1 = kege.search(taskId=2653)
task2 = kege.search(variantId=2832503195017, number_task=9)

variant = kege.search(variantId=2832503195017)
```
Получив объект нужного класса, вы можете, используя перечисленные выше атрибуты и методы, извлекать необходимую информацию. К примеру, в данном коде можно получить ответ задания `task1`, если обратиться к `task1.key`.
## [Открытие файлов](#openFiles)
```python
from kegepy import KEGE

kege = KEGE()

task = kege.search(taskId=2653)
file = task.open_file(file_number=1, printed=True, check_access=True)
```
С полученным файлом можно работать также, как и с обычным. При этом на ваш хост он не скачивается. Если файл не форматом .txt, то он автоматически конвертируется в него. Поддерживаются форматы ``.txt``, ``.xls``, ``.xlsx`` и ``.ods``.
Пример вывода в терминал при ``printed=True`` и ``check_access = True``:
```
-------------2653-------------

    File of task 2653 was loaded
    File name: 26.txt
    Symbols: 483
    Strings: 151
    
------------------------------
Access this file? (y/n). Default y:
```
## [Открытие изображений](#openImages)
```python
from kegepy import KEGE

kege = KEGE()

task = kege.search(taskId=2653)
task.open_image()
```
Изображение откроется отдельным окном. Поддерживаются форматы ``.png``, ``.jpg`` и ``.gif``.
