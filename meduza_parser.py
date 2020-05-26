# Парсер для извлечения всех статей и ссылок на них с информ агенства Медуза.io
# Используются в качестве инстурментов модули requests для get запроса к url и метод json для расспарсивания json объектов.

import requests
import json

url = 'https://meduza.io/api/w5/search?chrono=news&page={}&per_page=24&locale=ru'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
base_url = 'https://meduza.io/'

x = 0
while True:
	try:
		r = requests.get(url.format(x), headers=headers).text
		x +=1
		data_0 = [value for value in json.loads(r)['documents'].values()]

		for i in data_0:
			print(i['title'])
			print(base_url + i['url'])
	except:
		print('Больше ничего не нашли!')
		break
