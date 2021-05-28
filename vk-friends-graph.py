import requests
import os
import time

def get_user_info(user_id, fields, token, api_version):
  params = {'user_id' : int(user_id),
              'fields' : ','.join(fields),
              'name_case' : 'Nom',
              'v' : api_version,
              'access_token' : token}
  url = 'https://api.vk.com/method/users.get'

  try:
      req = requests.get(url, params=params)
      user = req.json()['response'][0]
  except:
      raise ValueError('Wrong user id or server error')
  
  return user

def make_dict_from_user_info(user, user_type):

  user_info = {}

  # Обязательные поля
  user_info['id'] = str(user['id'])
  user_info['name'] = (user['first_name'] + ' ' + user['last_name']).strip()
  user_info['type'] = str(user_type)
  user_info['gender'] = 'male' if user['sex'] == 2 else 'female'
  user_info['domain'] = 'vk.com/' + user['domain']

  # Необязательные поля
  user_info['country'] = user['country']['title'] if user.get('country') else 'Unknown'
  user_info['city'] = user['city']['title'] if user.get('city') else 'Unknown'
  user_info['bdate'] = user['bdate'] if user.get('bdate') else 'Unknown'

  return user_info

def make_node_from_user_info(user_info):
  new_node = []
  for key in user_info:
    new_node.append(user_info[key])
  new_node = ','.join(new_node)
  return new_node

def write_to_csv(filename, fields, rows):
  with open(filename, 'w', encoding='utf-8') as f:
    f.write(fields + '\n')
    for row in rows:
      f.write(row + '\n')

def request_friends(user_id, count, fields, token, api_version):
  url = f'https://api.vk.com/method/friends.get'
  params = {'v' : api_version,
            'access_token' : token,
            'user_id' : user_id,
            'count' : count,
            'fields' : ','.join(fields)}
  return requests.get(url, params=params).json()['response']

def is_mutual(friend, my_friends):
  for person in my_friends:
    if person['id'] == friend['id']:
      return True
  return False

token = os.environ.get('TOKEN')
if not token:
  print('Токен не найден в переменных окружения')
  token = input('Введите токен: ')

version = '5.131'
fields = ['sex', 'bdate', 'city', 'country', 'domain']

while True:
  user_id = input('Введите цифровой ID: ')

  print('Получение информации об аккаунте')

  try: 
    user = get_user_info(user_id, fields, token, version)
    user = make_dict_from_user_info(user, 'me')
    break
  except ValueError:
    print('Не удалось получить информацию')
    continue

print('Имя:', user.get('name'))

while True:
  try:
    print('Введите максимальное количество друзей для одного человека')
    print('(рекомендуется 100-250)')
    count = int(input('Ваш выбор: '))
    break
  except:
    print('Ошибка ввода, повторите.')

print('Получение списка друзей')

my_friends = request_friends(user_id, count, fields, token, version)['items']

print('Количество друзей:', len(my_friends))

edges = []

friends_of_friends = []
open_accounts = 0

for i, friend in enumerate(my_friends):
  mutual_friends = 1
  try:
      request = request_friends(friend.get('id'), count, fields, token, version)['items']
  except:
      continue
  
  open_accounts += 1
  
  for _friend in request:
    if is_mutual(_friend, my_friends):
      mutual_friends += 1
    friends_of_friends.append(_friend)
    edges.append(f"{friend['id']},{_friend['id']},1")

  edges.append(f"{user_id},{friend['id']},{mutual_friends}")
  print(f'Получение списка друзей друзей: {i+1}/{len(my_friends)}', end='\r')
  time.sleep(0.5)

print('\nЗакрытых аккаунтов среди друзей:', len(my_friends) - open_accounts)

nodes = []
nodes.append(make_node_from_user_info(user))

for friend in my_friends:
  friend = make_dict_from_user_info(friend, 'friend')
  nodes.append(make_node_from_user_info(friend))

for friend in friends_of_friends:
  friend = make_dict_from_user_info(friend, 'friend_of_friend')
  new_node = make_node_from_user_info(friend)

  if new_node not in nodes:
    nodes.append(new_node)

print(f'Количество вершин: {len(nodes)}. Запись в файл nodes.csv')
write_to_csv('nodes.csv', 'id,label,type,sex,domain,country,city,bdate', nodes)

print(f'Количество рёбер: {len(edges)}. Запись в файл edges.csv')
write_to_csv('edges.csv', 'source,target,weight', edges)

input('Готово!')
