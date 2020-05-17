from datetime import datetime
import requests
from bs4 import BeautifulSoup as BS 
import csv

URL = 'https://www.dns-shop.ru/catalog/17aa522a16404e77/komplektuyushhie-dlya-pk/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
base_url = 'https://www.dns-shop.ru'

def get_url_pc_item(url, headers):
	sec = requests.Session()
	req = sec.get(url, headers=headers)
	return req.text

def get_list_of_items(html):
	soup = BS(html, 'lxml')

	names = []
	all_href = []

	table = soup.find_all('a','subcategory__item ui-link ui-link_blue')
	for i in table:
		href =  base_url + i.get('href')
		all_href.append(href)
		name = i.find('label', 'subcategory__mobile-title').text.upper()
		names.append(name)

	spisok = dict(zip(names, all_href))
	return spisok

def decision(letter, a_list):
	letter = letter
	while letter not in a_list:
		print('Вы не выбрали из списка данного списка желаемую позицию:\n', a_list[:4])
		letter = input().upper()
	return letter

def get_url_of_pars(letter,spisok):
	find_url = spisok[letter]
	print('-'*10)
	print('Начинаем парсинг')
	print('-'*10)
	return find_url

def get_count_pages(find_url, headers):
	sec = requests.Session()
	req = sec.get(find_url, headers=headers)
	html = req.text

	soup = BS(html, 'lxml')
	last_page = soup.select('li.pagination-widget__page')[-1]
	pages = int(last_page.get('data-page-number'))
	return pages

def a_params(pages):
	params = {
	'order': 1,
	'stock': 2,
	'p': None # изначально нет страницы
	}
	if pages >1:
		params['p'] = pages
	return params

def get_links(pages, params, headers, find_url):
	
	urls = []

	for x in range(1, pages + 1):
		
		params['p'] = x

		print('Сканируем %s' %(x), 'страницу', '.'*x)

		sec = requests.Session()
		req = sec.get(find_url, params=params, headers=headers)
		html = req.text

		soup = BS(html, 'lxml')
		items = soup.select('div.n-catalog-product__main')
		for item in items:
			link = base_url + item.find('a', {'class':'ui-link'})['href']
			urls.append(link)
	print('-'*10)		
	print('Всего найдено %s' %(len(urls)), 'товаров.')
	print('-'*10)
	return urls

def get_list_items(urls, headers):
	print('Начинаем парсить товары:')
	data = []

	for u in urls:
		print('Товар № %s' %(len(data) +1), 'из %s' %(len(urls)), 'Осталось %s' %(len(urls) - len(data) -1))
		sec = requests.Session()
		req = sec.get(u, headers=headers)
		html = req.text

		soup = BS(html, 'lxml')
		content = soup.select('div.clearfix')
		for i in content:
			price = i.select_one('span.current-price-value').text.strip() + 'RU'
			name = i.select_one('span.name').text.strip()
			try:
				rating = i.select_one('div.product-item-rating').get('data-rating') + ' /5'
			except:
				rating = 0
			data.append([name, price, rating])
	return data

def get_csv(data):
	names = ['Название', 'Цена', 'Рейтинг']
	with open('блоки_питания.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(names)
		for i in data:
			writer.writerow(i)
	return i

print('-'*10)
print('Это парсер магазина DNS!')
print('-'*10)
print('Напишите, что Вы хотите спарсить? Вы можете спарсить следующие позиции:\t') 


while True:
	print('ПРОЦЕССОРЫ, МАТЕРИНСКИЕ ПЛАТЫ, ВИДЕОКАРТЫ, БЛОКИ ПИТАНИЯ, КОРПУСА')
	print('-'*10)
	letter = input().upper()
	a_list = ['ПРОЦЕССОРЫ', 'МАТЕРИНСКИЕ ПЛАТЫ', 'ВИДЕОКАРТЫ', 'БЛОКИ ПИТАНИЯ', 'КОРПУСА', 'НЕТ']
	dec = decision(letter, a_list)
	start_time = datetime.now()
	if dec in a_list[:4]:
		spisok = get_list_of_items(get_url_pc_item(URL, HEADERS))
		find_url = get_url_of_pars(letter, spisok)
		pages = get_count_pages(find_url, HEADERS)
		pam = a_params(pages)
		get_links = get_links(pages, pam, HEADERS, find_url)
		all_data =  get_list_items(get_links, HEADERS)
		file = get_csv(all_data)
		
		print('-'*10)
		print('Все получилось!')
		print(datetime.now() - start_time)
		print('-'*10)
		print('Хотите пропарсить еще раз? да или нет')
		
		if not input().startswith('д'):
			break

	if dec == 'НЕТ':
		print('До свидания!')
		break


	



	







