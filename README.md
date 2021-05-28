
# Создание графов друзей Вконтакте

![Black](https://github.com/CosmoSt4r/vk-friends-graph/blob/master/readme/example-black.png?raw=true)
__________

## Как установить?

Для работы скрипта необходима библиотека `requests`
```py
pip install requests
```
Также, нужно получить собственный токен от VK API. [Как его получить?](https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/) Токен можно записать в переменную окружения или передать скрипту вручную, когда он будет запрошен. <br>
Программа, использующаяся для визуализации графа - [Gephi](https://gephi.org/)

__________
## Как пользоваться?

Для построения графа понадобится цифровой ID пользователя ВК. [Как его найти?](https://vk.com/faq18062) <br>
Далее необходимо выбрать максимальное количество друзей для каждого человека. Максимум: 5000, но рекомендую ставить от 100 до 250, так как люди с количеством друзей больше 2-3 тысяч будут засорять граф. <br>
Затем можно выбрать, добавлять ли людей без общих с вами друзей или нет. После ответа на данный вопрос скрипт начнет собирать друзей ваших друзей и сохранит их в файл `nodes.csv`. Связи между друзьями будут сохранены в `edges.csv`. <br>
После завершения работы скрипта, он предложит конвертировать конвертировать эти два файла в GraphML формат, чтобы получить один файл. Для этого понадобится файл `csv_to_gml.py`. <br>
Затем просто импортируем полученный файл в Gephi, немного **магии** и получаем красивые визуализации.

![White](https://github.com/CosmoSt4r/vk-friends-graph/blob/master/readme/example-white.png?raw=true)

______

