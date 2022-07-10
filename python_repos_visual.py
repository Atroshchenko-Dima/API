import requests
from plotly.graph_objs import Bar
from plotly import offline
from tables import Description

# Создание вызова API исохранение овтета
url = 'https://api.github.com/search/repositories?q=language:Python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'} # т.к гитхаб использует 3ю версию API, определяются заголовки
# Модуль requests используется для вызова. 
r = requests.get(url, headers=headers) # Вызываем метод get() и передаем ему url и заголовок, а объект ответа сохраняется в переменной r
print(f"Status code: {r.status_code}") # объект ответа содержит атрибут status_code, в нем хранится признак успешного выполнения запроса(код 200) 

# Сохранение ответа API в переменной
response_dict = r.json() # т.к API возвращает информацию в формате json, используем метод json() для преобразования информации в словарь python
# выводится значение связанное с total count - представляющее общее кол-во репозиториев python в github
print(f"Total repositories: {response_dict['total_count']}") 

# Обработка результатов
repo_dicts = response_dict['items'] # items представляет собой список со словарями, которые содержат данные об одном из репозиториев python
# создаем 3 пустых списка для хранения данных, включаемых в диаграмму. Имя проекта(для пометки столбцов) и кол-во звезд, определяющее высоту столбцов
repo_links, stars, labels = [], [], [] 
for repo_dict in repo_dicts: # перебираются все словари в repo_dicts.
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url'] # извлекаем URL-адрес проекта и присваиваем его временной переменной
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>" # генерируется ссылка на проект
    repo_links.append(repo_link) # присоединение ссылки к списку
    stars.append(repo_dict['stargazers_count'])
# сделаем экранную подсказку при наведении курсора на столбец в диаграмме(описание проекта)
    owner = repo_dict['owner']['login'] # извекаем владельца и описание для каждого проекта
    description = repo_dict['description']
    label = f"{owner}<br />{description}" # <br /> - текст с разрывом строки
    labels.append(label)

# Построение визуализации. Словарь data определяет тип диаграммы и содержит значения по осям х и у
data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    'hovertext': labels,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6
}]
# Cловарь с нужными спецификациями макета. Заголовок и подписи осей
my_layout = {
    'title': 'Most-Starred Python Projects on GitHub',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Repository',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Stars',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}
fig = {'data': data, 'layout':  my_layout}
offline.plot(fig, filename = 'python_repos.html')