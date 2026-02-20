import urllib.request
import pandas as pd
from io import BytesIO, TextIOWrapper
from requests import get
from dataclasses import dataclass
from PIL import Image



URLS_KOMPEGE = {
    "main": "https://kompege.ru/api/v1/",
    "file": "https://kompege.ru/files/",
    "user_id": "https://kompege.ru/api/v1/result/",
    "task": "task/",
    "variant": "variant/kim/",
    "image": "https://kompege.ru/images/"
}
HEADERS_DEFAULT = {'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 '               'Firefox/14.0.1'),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3','Accept-Encoding':'gzip, deflate','Connection':'keep-alive','DNT':'1',
                   'Content-Type': 'application/json; charset=utf-8',
                   'Cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0',
                   'Access-control-allow-credentials': 'true',
                    'Access-control-allow-origin': 'https://kompege.ru',
                    "grant_type" : "client_credentials"
                   }

@dataclass
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

    def get_answers(self):
        data = list()
        ms = [26, 27]

        for t in self.tasks:
            n, tI, ans = t["number"], t["taskId"], t["key"]
            data.append({"answer": ans, "taskId": tI, "score": (2 if n in ms else 1), "number": n})
        return data
    def get_task(self, number):
        if 27 >= number >= 1: return Task(**self.tasks[number-1])

@dataclass
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

    def get_files_names(self) -> list: return [{"url": file["url"].split('/')[-1], "name": file["name"]} for file in self.files]

    def open_file(self, file_number : int = 1, printed : bool = 0, check_access : bool = 0) -> TextIOWrapper:
        names = self.get_files_names()
        if len(names) < file_number:
            print("KEGEPY: Files weren't found :(")
            return 0

        file_name, real_name = names[file_number-1].values()
        extension = file_name.split('.')[-1]

        resp = urllib.request.urlopen(URLS_KOMPEGE["file"] + file_name)
        content = resp.read()

        if extension in ("xls", "xlsx", "ods"):
            content = pd.read_excel(BytesIO(content)).to_csv(sep=' ', index=False, header=True, encoding="utf-8").encode()
        elif extension != "txt":
            print(f"KEGEPY: .{extension} is not supported :(")
            return 0
        file = TextIOWrapper(BytesIO(content), encoding="utf-8")

        if printed:
            ou_con = content.decode()
            L_symb, L_str = len(ou_con), ou_con.count('\n') + (1 if ou_con[-1:] != '\n' else 0)
            L_symb -= L_str

            pr = \
    f"""
    File of task {self.taskId} was loaded
    File name: {real_name}
    Symbols: {L_symb}
    Strings: {L_str}
    """
            l_mx = len(max(pr.split('\n'), key=len))
            koef = (l_mx//2) - (len(str(self.taskId))-1)
            print('-'*koef + str(self.taskId) + '-'*koef)
            print(pr)
            print('-'*koef*2 + '-'*len(str(self.taskId)))
        if check_access: 
            if input("Access this file? (y/n). Default y: ") == 'n': return 0
        return file
    def open_example(self) -> TextIOWrapper:
        if self.number == 26:
            content = ""
            try: s_t = self.text.index('<em>Типовой пример')
            except ValueError: return 0
            e_t = self.text.index('</em>', s_t)
            l = self.text[e_t:].replace('</em><br />', '~').replace('<em>', '').split('~')
            for li in l:
                li = li.strip()
                if li == '': continue
                if not li.replace(' ', '').isdigit(): break
                content += (li + '\n')
            file = TextIOWrapper(BytesIO(content[:-1].encode()), encoding="utf-8")
            return file
    def open_image(self):
        resp = get(URLS_KOMPEGE["image"] + str(self.taskId) + '.png', stream=True)
        resp.raw.decode_content = True
        return Image.open(resp.raw).show()




    
class KEGE:
    def __init__(self, headers: dict = HEADERS_DEFAULT):
        self.headers = headers

    def search(self, taskId: int = 0, variantId: int = 0, number_task: int = 0): 
        search_type = "task_taskId"
        code = 0

        if (taskId or variantId or number_task) is False: return None
        else:
            if taskId: 
                response = get(URLS_KOMPEGE["main"] + URLS_KOMPEGE["task"] + str(taskId), headers=self.headers)
                if response.status_code < 400: 
                    return Task(**self.__data_extraction__(response.json(), search_type))
                else: code = response.status_code
            if variantId:
                response, search_type = get(URLS_KOMPEGE["main"] + URLS_KOMPEGE["variant"] + str(variantId), headers=self.headers), "variant"
                if response.status_code < 400:
                    if number_task:
                        if 27 >= number_task >= 1:
                            search_type = "task_variantId"
                            return Task(**self.__data_extraction__(response.json(), search_type, number_task))
                        else:
                            print(f"KEGEPY: Number {number_task} is too large.")
                            return None
                    return Variant(**self.__data_extraction__(response.json(), search_type))
                else: code = response.status_code
        print(f"KEGEPY: Not found. Code: {code}")
        return None
    def __data_extraction__(self, data : dict, search_type: str, *args) -> dict:
        if search_type == "task_variantId": return data["tasks"][args[0]-1]
        return data