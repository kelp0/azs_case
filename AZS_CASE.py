#Работу выполниили: Скороходов М. 80%, Лысенко М. 50%, Ячин Д. 30%
import random
from typing import List, Any
import pprint

azs = open('azs.txt', 'r')
inp = open('input.txt', 'r')
informationaboutazs: list[str] = azs.readlines()
prices = {'АИ-80': 43, 'АИ-92': 46, 'АИ-95': 50, 'АИ-98': 59}
petrol = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
carswithoutservice = 0

# Информация по заправке
for i in range(len(informationaboutazs)):
    informationaboutazs[i] = informationaboutazs[i].split()
    informationaboutazs[i][0] = int(informationaboutazs[i][0])
    informationaboutazs[i][1] = int(informationaboutazs[i][1])

# Информация по клиентам
inp_l: list[Any] = list(map(lambda x: x.strip(), inp.readlines()))
for i in range(len(inp_l)):
    inp_l[i] = inp_l[i].split()
    inp_l[i][1] = int(inp_l[i][1])
azs_filling = {informationaboutazs[i][0]: 0 for i in range(len(informationaboutazs))}
azs_free = {informationaboutazs[i][0]: informationaboutazs[i][1] for i in range(len(informationaboutazs))}


# Получаем время
def timing(times, minutes=0):
    times = times.split(':')
    hours: int = int(times[0])
    mins: int = int(times[1])
    minutes = hours * 60 + mins
    return minutes


# Переводим время в нужную величину
def time_manage(minutes):
    s = ''
    hours = minutes // 60
    l_minutes = minutes - hours * 60
    if len(str(hours)) != 1:
        s += str(hours)
    else:
        s += '0{0}'.format(str(hours))
    if len(str(l_minutes)) != 1:
        s += ':{0}'.format(str(l_minutes))
    else:
        s += ':0{0}'.format(str(l_minutes))
    return s


# Прибытие новой машины на АЗС
def new(i, type_petrol, number_of_gas):
    print(
        f'В {str(i[0])} новый клиент {str(i[0])} {type_petrol} {i[1]} {fill_final_time} встал в очередь к автомату №{str(number_of_gas)}')
    azs_filling[number_of_gas] += 1
    petrol[type_petrol] += i[1]


time_orders = []
for minute in range(1, 1441):
    for _ in time_orders:
        for ch1 in time_orders:
            if ch1[1] == minute:
                print(
                    f'В {time_manage(ch1[1])} клиент {time_manage(ch1[0])} {ch1[2]} {str(ch1[3])} {str(ch1[4])} заправил свой автомобиль и покинул АЗС')
                azs_filling[ch1[5]] -= 1
                time_orders.remove(ch1)
                for i in range(len(informationaboutazs)):
                    print('Автомат №' + str(informationaboutazs[i][0]) + ' максимальная очередь: ' + str(
                        informationaboutazs[i][1]) + ' Марки бензина: ' + ' '.join(
                        informationaboutazs[i][2::]) + ' ->' + azs_filling[i + 1] * '*')
    for i in inp_l:
        c = 0
        time = i[0]
        time_in_minutes = timing(time)
        litres = i[1]
        add = random.randint(-1, 1)
        if 0 == litres % 10:
            if 0 != litres // 10 + add:
                fill_final_time = litres // 10 + add
            elif litres // 10 + add == 0:
                fill_final_time = 1
        elif litres % 10 != 0:
            if litres // 10 + add != 0:
                fill_final_time = litres // 10 + add + 1
            elif litres // 10 + add == 0:
                fill_final_time = 1
        type_petrol = i[2]
        if minute != time_in_minutes:
            continue
        for gas in informationaboutazs:
            for j in gas[2::]:
                if type_petrol != j or azs_free[gas[0]] <= azs_filling[gas[0]] or c != 0:
                    continue
                num_of_gas = gas[0]
                new(i, type_petrol, gas[0])
                c += 1
                break
        if c != 0:
            ch = [time_in_minutes, time_in_minutes + fill_final_time, type_petrol, litres, fill_final_time,
                  num_of_gas]
            time_orders.append(ch)
        else:
            carswithoutservice += 1
            print(
                f'В {time} новый клиент {time} {type_petrol} {str(litres)} {str(fill_final_time)} не смог заправить автомобиль и покинул АЗС')
        for i in range(len(informationaboutazs)):
            print('Автомат №' + str(informationaboutazs[i][0]) + ' максимальная очередь: ' + str(
                informationaboutazs[i][1]) + ' Марки бензина: ' + ' '.join(informationaboutazs[i][2::]) + ' ->' +
                  azs_filling[i + 1] * '*')
# Вывод финального ответа
def print0(petrol):
    print("Количество литров, проданное за сутки по каждой марке бензина:")
    for item, amount in petrol.items():
        print(f'{item}: {amount} литров')
print('-'*100)
print0(petrol)
print('-'*100)
d = {k: v * petrol[k] for k, v in prices.items() if k in petrol}
def print1(d):
    print("Прибыль по каждой марке бензина:")
    for item, amount in d.items():
        print(f'{item}: {amount} рублей')
print1(d)
print('-'*100)
print(f'Общая сумма продаж за сутки в рублях: {sum(d.values())} рублей')
print('-'*100)
print("Количество клиентов, которые покинули АЗС не заправив автомобиль из-за «скопившейся» очереди:", carswithoutservice)
print('-'*100)
