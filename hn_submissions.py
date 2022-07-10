from operator import itemgetter
import requests
from plotly.graph_objs import Bar
from plotly import offline

# Создание вызова API и сохранение ответа
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Обработка информации о каждой статье
submission_ids = r.json() # текст ответа преобразуется в список python и сохраняем в переменной
submission_dicts = [] # пустой список для хранения словарей
# Программа перебирает идентификаторы 30 самых популярных статей и выдает новый вызов API для каждой статьи, генерируя URL  с текущим значением submission_id
for submission_id in submission_ids[:30]:
    # Создание отдельного вызова API для каждой статьи
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()
    try:
    # Построение словаря для каждой статьи. В нем сохраняется заголовок/ссылка на страницу/колличество комментариев
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
    except KeyError:
        # This is a special post with comments disabled.
        continue
    else:
        submission_dicts.append(submission_dict)

# key=itemgetter('comments') - извлекает значение, связанное с данным ключем, из каждого словаря в списке
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# после того как список отсортирован, перебираем элементы и выводим для каждой из самых популярных статей 3 атрибута
titles, comments = [], []
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    titles.append(submission_dict['title'])
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")
    comments.append(submission_dict['comments'])

# Построение визуализации. Словарь data определяет тип диаграммы и содержит значения по осям х и у
data = [{
    'type': 'bar',
    'x': titles,
    'y': comments,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6
}]
# Cловарь с нужными спецификациями макета. Заголовок и подписи осей
my_layout = {
    'title': 'Most commented news on hacker-news',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Denominations',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Comments',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}
fig = {'data': data, 'layout':  my_layout}
offline.plot(fig, filename = 'hn.html')