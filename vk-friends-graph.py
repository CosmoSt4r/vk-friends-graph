import requests
import os
import time

token = 'your token'
version = '5.130'
offset = 0
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
    

print('Имя:', user_name)
print('Получение списка друзей')

url = f'https://api.vk.com/method/friends.get'
count = 100

my_followers = []

params = {'v' : version,
          'access_token' : token,
          'user_id' : user_id,
          'offset' : offset,
          'count' : count,
          'fields' : ','.join(fields)}
req = requests.get(url, params=params)
  
for follower in req.json()['response']['items']:
  my_followers.append(follower)

print('Количество друзей:', len(my_followers))

edges = []
followers_second = []

open_accounts = 0
for i, follower in enumerate(my_followers):
    offset = 0

    params = {'v' : version,
              'access_token' : token,
              'user_id' : follower['id'],
              'offset' : offset,
              'count' : count,
              'fields' : fields.replace(' ', '')}
    req = requests.get(url, params=params)
    
    try:
        response = req.json()['response']['items']
    except:
        continue

    open_accounts += 1
    for _follower in response:
        followers_second.append(_follower)
        edges.append(f"{follower['id']},{_follower['id']}")

    print(f'Получение списка друзей друзей: {i+1}/{len(my_followers)}', end='\r')
    time.sleep(0.5)

for follower in my_followers:
  edges.append(f"{user_id},{follower['id']}")

print()
print('Закрытых аккаунтов среди друзей:', len(my_followers) - open_accounts)

nodes = []

nodes.append(f'{user_id},{user_name},me,{user_gender}')

for follower in my_followers:
  _id = str(follower['id'])
  username = (follower['first_name'] + ' ' + follower['last_name']).strip()
  type_ = 'friend'
  sex = 'male' if follower['sex'] == 2 else 'female'

  nodes.append(','.join([_id, username, type_, sex]))

for follower in followers_second:
  _id = str(follower['id'])
  username = (follower['first_name'] + ' ' + follower['last_name']).strip()
  type_ = 'friend_of_friend'
  sex = 'male' if follower['sex'] == 2 else 'female'

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
