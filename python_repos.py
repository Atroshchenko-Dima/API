import requests

# Создание вызова API исохранение овтета
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'} # т.к гитхаб использует 3ю версию API, определяются заголовки
# Модуль requests используется для вызова. 
r = requests.get(url, headers=headers) # Вызываем метод get() и передаем ему url и заголовок, а объект ответа сохраняется в переменной r
print(f"Status code: {r.status_code}") # объект ответа содержит атрибут status_code, в нем хранится признак успешного выполнения запроса(код 200) 

# Сохранение ответа API в переменной
response_dict = r.json() # т.к API возвращает информацию в формате json, используем метод json() для преобразования информации в словарь python
# выводится значение связанное с total count - представляющее общее кол-во репозиториев python в github
print(f"Total repositories: {response_dict['total_count']}") 

# Анализ информации о репозиториях
repo_dicts = response_dict['items'] # items представляет собой список со словарями, которые содержат данные об одном из репозиториев python
 # выводит длину repo_dicts, чтоб пользователь видел, по какому кол-ву репозиториев есть информация
print(f"Repositories returned: {len(repo_dicts)}")


# Анализ первого репозитория
repo_dict = repo_dicts[0] # чтоб получить первое представление об информации, возвращенной по каждому репозиторию
print("\nSelected information about each repository:")
for repo_dict in repo_dicts: # перебираются все словари в repo_dicts
    print(f"\nName: {repo_dict['name']}")
    print(f"Owner: {repo_dict['owner']['login']}")
    print(f"Stars: {repo_dict['stargazers_count']}")
    print(f"Repository: {repo_dict['html_url']}")
    print(f"Created: {repo_dict['created_at']}")
    print(f"Updated: {repo_dict['updated_at']}")
    print(f"Description: {repo_dict['description']}")
