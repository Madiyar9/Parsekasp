# Чтение ссылок из файла output1.txt
with open(r'C:\Users\Мадияр\Desktop\output1.txt', 'r', encoding='utf-8') as file1:
    links1 = set(line.strip() for line in file1)

# Чтение ссылок из файла notebooks30.csv
import pandas as pd

df = pd.read_csv(r'C:\Users\Мадияр\Desktop\notebooks30.csv')
links2 = set(df['Link'])

# Найти ссылки, которые есть в links1, но отсутствуют в links2
missing_in_links2 = links1 - links2

# Найти ссылки, которые есть в links2, но отсутствуют в links1
missing_in_links1 = links2 - links1

# Вывести отсутствующие ссылки
print("Ссылки, отсутствующие в файле notebooks30.csv, но есть в output1.txt:")
for link in missing_in_links2:
    print(link)

print("\nСсылки, отсутствующие в output1.txt, но есть в файле notebooks30.csv:")
for link in missing_in_links1:
    print(link)
