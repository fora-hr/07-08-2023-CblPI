from typing import NamedTuple
from datetime import datetime
from json import load



class Participant(NamedTuple):

    number: int
    scoretime: datetime
    surname: str
    name: str


def format_print_data(participants: list):
    
    print("|  Занятое место  | Нагрудный ",
        end="номер |     Имя     |    Фамилия   |    Результат    |\n")
    print("|-----------------+-----------------+-----",
        end="--------+--------------+-----------------|\n")

    for place, obj in enumerate(participants, 1):
        print('|', ' | '.join([
            f'{str(place):15}', f'{obj.number:15}', f'{obj.name:11}',
            f'{obj.surname:12}',
            f'{str(obj.scoretime)[2:10]:15}']), '|')


def get_data(competitors: str, result: str) -> list:
    
    result_list = []
    
    with open(competitors, 'r') as file_json:
        data_json = load(file_json)

    with open(result, 'r') as file_txt:
        data_txt_ln = file_txt.read().split('\n')
        
    second_time : datetime = None
    
    for line in data_txt_ln:

        if not line:
            continue
        
        num, _, time = line.split(" ")
        
        time: datetime = datetime.strptime(time.strip(),
                                           "%H:%M:%S,%f")
        
        if second_time is None:
            second_time = time
            continue

        result_list.append(Participant(num,
                                    (second_time - time)* - 1,
                                    data_json.get(num).get("Name"),
                                    data_json.get(num).get("Surname")))
        
        second_time = None
    
    list_res_sort = sorted(result_list, key=lambda sortby: sortby[1])

    return list_res_sort
    
format_print_data(get_data('competitors2.json','results_RUN.txt'))
