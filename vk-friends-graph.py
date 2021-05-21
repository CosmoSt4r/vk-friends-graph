import requests
import os
import time

token = os.environ.get('TOKEN')
version = '5.131'
fields = ['sex', 'bdate', 'city', 'country', 'domain']

while True:
    user_id = input('Введите цифровой ID: ')

    print('Получение информации об аккаунте')
    
    params = {'user_id' : int(user_id),
              'fields' : ','.join(fields),
              'name_case' : 'Nom',
              'v' : version,
              'access_token' : token}
    url = 'https://api.vk.com/method/users.get'

    try:
        req = requests.get(url, params=params)
        user = req.json()['response'][0]
    except:
        print('Не удалось получить информацию')
        continue
    
    # Обязательные поля
    user_name = (user['first_name'] + ' ' + user['last_name']).strip()
    user_gender = 'male' if user['sex'] == 2 else 'female'
    user_domain = user['domain']

    # Необязательные поля
    user_country = user['country']['title'] if user.get('country') else 'Unknown'
    user_city = user['city']['title'] if user.get('city') else 'Unknown'
    user_bdate = user['bdate'] if user.get('bdate') else 'Unknown'

    break
    

print('Имя:', user_name)

while True:
  try:
    print('Введите максимальное количество друзей для одного человека')
    print('(рекомендуется 100-250)')
    count = int(input('Ваш выбор: '))
    break
  except:
    print('Ошибка ввода, повторите.')

print('Получение списка друзей')

url = f'https://api.vk.com/method/friends.get'

my_friends = []

params = {'v' : version,
          'access_token' : token,
          'user_id' : user_id,
          'count' : count,
          'fields' : ','.join(fields)}
req = requests.get(url, params=params)

for friend in req.json()['response']['items']:
  my_friends.append(friend)

print('Количество друзей:', len(my_friends))

edges = []
friends_of_friends = []

open_accounts = 0
for i, friend in enumerate(my_friends):
    offset = 0

    params = {'v' : version,
              'access_token' : token,
              'user_id' : friend['id'],
              'count' : count,
              'fields' : ','.join(fields)}
    req = requests.get(url, params=params)
    
    try:
        response = req.json()['response']['items']
    except:
        continue

    open_accounts += 1
    for _friend in response:
        friends_of_friends.append(_friend)
        edges.append(f"{friend['id']},{_friend['id']}")

    print(f'Получение списка друзей друзей: {i+1}/{len(my_friends)}', end='\r')
    time.sleep(0.5)

for friend in my_friends:
  edges.append(f"{user_id},{friend['id']}")

print('\nЗакрытых аккаунтов среди друзей:', len(my_friends) - open_accounts)

nodes = []

nodes.append(f'{user_id},{user_name},me,{user_gender}')

for friend in my_friends:
  _id = str(friend['id'])
  username = (friend['first_name'] + ' ' + friend['last_name']).strip()
  type_ = 'friend'
  sex = 'male' if friend['sex'] == 2 else 'female'

  nodes.append(','.join([_id, username, type_, sex]))

for friend in friends_of_friends:
  _id = str(friend['id'])
  username = (friend['first_name'] + ' ' + friend['last_name']).strip()
  type_ = 'friend_of_friend'
  sex = 'male' if friend['sex'] == 2 else 'female'

  new_f = ','.join([_id, username, type_, sex])

  if new_f not in nodes:
    nodes.append(new_f)

print('Количество вершин:', len(nodes))
print('Количество рёбер:', len(edges))

print('Запись вершин в файл nodes.csv')
with open('nodes.csv', 'w', encoding='utf-8') as f:
  f.write('id,label,type,sex\n')
  for node in nodes:
    f.write(node + '\n')

print('Запись ребер в файл edges.csv')
with open('edges.csv', 'w', encoding='utf-8') as f:
  f.write('source,target\n')
  for edge in edges:
    f.write(edge + '\n')

input('Готово!')
