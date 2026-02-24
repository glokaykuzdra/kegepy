# Грокаем KEGE с помощью Python.
Библиотека **kegepy** предназначена для работы с сервисом [kompege.ru](https://kompege.ru) (КЕГЭ). С ее помощью вы сможете легко получить данные того или иного задания или варианта. Здесь предоставляется возможность использовать файлы без прямого скачивания на компьютер, открывать изображения, получать ответы и т.д.

- [Kлассы](#classes)
  - [KEGE](#kege)
  - [Task](#task)
  - [Variant](#variant)
  - [File](#file)
  - [Image](#image)
- [Начало работы](#firstWork)
  - [Открытие файлов](#openFiles)
  - [Открытие изображений](#openImages)

<a name="classes"></a>
# [Kлассы](#classes)
Ниже описаны основные классы библиотеки. Считайте этот пункт небольшой документацией.
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

Метод возвращает в зависимости от входных параметров классы [`Task`](#task) или [`Variant`](#variant). Для получения класса `Task` необходимо передать `taskId` или `variantId` с `number_task`. В случае с классом `Variant` передается `variantId`.
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
    headers: dict
```
### .get_files_names()
`Task(**kwargs).get_files_names()`  
Метод возвращает список из словарей, имеющие такие ключи:  
- `url`: имя файла на сервере kompege.
- `name`: имя файла при скачивании.
### .get_file()
`Task(**kwargs).get_file(file_number: int = 1)`  
- `file_number`: порядковый номер файла, который будет открыт.   

Метод возвращает класс [`File`](#file).
### .open_example()
`Task(**kwargs).open_example()`  
Метод возвращает класс `TextIOWrapper`. Используется для извлечения типового примера из заданий типа 26.  
### .open_image()
`Task(**kwargs).open_image()`  
Метод возвращает класс [`Image`](#image)
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
    headers: dict
```
### .get_task()
`Variant(**kwargs).get_task(number : int)`  
- `number`: номер типа задания из варианта.

Метод возвращает класс [`Task`](#task).
### .get_answers()
`Variant(**kwargs).get_answers()`  
Метод возращает список из словарей, содержащих следующие ключи:  
- `answer`: ответ на задание.
- `taskId`: айди задания.
- `score`: максимальное количество баллов за выполнение задания.
- `number`: номер типа задания.

## [File](#file)
```python
class File:
    url: str
    filename: str
    filename_server: str
    extension: str
    taskId: int
    html: str
    headers: dict
```
### .open()  
`File(**kwargs).open(encoding : str = "utf-8", printed : bool = 0)`  
- `encoding`: кодировка информации файла.
- `printed`: вывод дополнительной информации.

Метод возвращает класс `TextIOWrapper`. Открываемый файл конвертируется в формат `.txt`. Для таблиц **excel** столбцы разделяются по пробелу. Поддерживаются форматы `xls`, `xlsx`, `ods` и `txt`.
### .download()
`File(**kwargs).download(self, encoding : str = "utf-8", path : str = '.\\')`  
- `encoding`: кодировка информации файла.
- `path`: путь, по которому сохранится файл.

Метод загружает файл по указанному пути (если путь не указан, то файл сохранится там же, где и модуль kegepy). Файл автоматически конвертируется в формат `.txt`. Для таблиц **excel** столбцы разделяются по пробелу. Поддерживаются форматы `xls`, `xlsx`, `ods` и `txt`.
## [Image](#image)
Наследует те же атрибуты, что и класс [`File`](#file)
### .open()
`Image(**kwargs).open()`  
Метод возвращает изображение в виде шестнадцатеричного кода.  
### .web_open()
`Image(**kwargs).web_open()`  
Метод открывает изображение в браузере, выбранном по умолчанию на устройстве. Есть проблемы с открытием изображений, сохраненных в формате base64.
### .download()
`Image(**kwargs).download(self, path : str = '.\\')`  
- `path`: путь, по которому сохранится изображение.

Метод загружает файл с расширением `.png` по указанному пути (если путь не указан, то файл сохранится там же, где и модуль kegepy).
<a name="firstWork"></a>
# [Начало работы](#firstWork)
Для использования необходимо установить зависимости, указанные в файле `requirements.txt`.
```
pip install -r requirements.txt
```
Для получения объекта задания [`Task`](#task) или варианта [`Variant`](#variant) необходимо знать их айди (номера). Айди варианта является номером кима, например `2832503195017`. Айди задания можно узнать в базе заданий КЕГЭ, например `2653`.  
```python
from kegepy import KEGE

kege = KEGE()

task1 = kege.search(taskId=2653)
task2 = kege.search(variantId=2832503195017, number_task=9)

variant = kege.search(variantId=2832503195017)
```
Получив объект нужного класса, вы можете, используя перечисленные выше атрибуты и методы, извлекать необходимую информацию. К примеру, в данном коде можно получить ответ задания `task1`, если обратиться к `task1.key`.
<a name="openFiles"></a>
## [Открытие файлов](#openFiles)
```python
from kegepy import KEGE

kege = KEGE()

task = kege.search(taskId=2653)
file_obj = task.get_file(file_number=1)

file = file_obj.open_file(printed=True)
```
Метод `.get_file` возвращает класс [`File`](#file).
С полученным файлом `file` можно работать так же, как и с обычным. При этом на ваш хост он не скачивается. Если файл не форматом `.txt`, то он автоматически конвертируется в него. Поддерживаются форматы `.txt`, `.xls`, `.xlsx` и `.ods`.
Пример вывода в терминал при `printed=True`:
```
-------------2653-------------
    File of task 2653 was loaded
    File name: 26.txt
    Symbols: 483
    Strings: 151
------------------------------
```
Файл также можно загрузить в папку с модулем kegepy или на указанный путь: `file.download(path="your_path")`. Формат загруженного файла `.txt`.  
Для заданий с номером типа 26 есть возможность загружать типовой пример из текста, который будет представлять из себя текстовый файл:
```python
from kegepy import KEGE

kege = KEGE()

task = kege.search(taskId=2653)
file = task.open_example()
```
В отличие от метода `.get_file()`, метод `.open_example()` возвращает класс `TextIOWrapper`.
<a name="openImages"></a>
## [Открытие изображений](#openImages)
```python
from kegepy import KEGE

kege = KEGE()

task = kege.search(taskId=2653)
image = task.get_image()

image.web_open() 
```
Метод `.get_image` возвращает класс [`Image`](#image).
Изображение `image` откроется отдельным окном в браузере, установленном по умолчанию. Однако `.web_open()` не работает корректно со всеми изображениями. Файл изображения можно загрузить в папку с модулем kegepy или на указанный путь: `image.download(path="your_path"`. Формат загруженного файла `.png`.
