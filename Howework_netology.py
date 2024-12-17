import os
from pprint import pprint

def cook_book_from_file(path):
    cook_book = {}
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            dish_name = f.readline().strip()
            if not dish_name:
                break
            count = int(f.readline().strip())
            ingredients = []
            for _ in range(count):
                ingredient_line = f.readline().strip()
                ingredient_name, quantity, measure = ingredient_line.split(' | ')
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'quantity': int(quantity),
                    'measure': measure
                })
            cook_book[dish_name] = ingredients
            f.readline()  # Пропускаем пустую строку между рецептами
    return cook_book

def get_shop_list_by_dishes(cook_book, dishes, person_count):
    ingr_list = {}
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                ingredient_name = ingredient['ingredient_name']
                quantity = ingredient['quantity'] * person_count
                measure = ingredient['measure']
                
                # Используем метод setdefault для добавления или обновления ингредиента
                if ingredient_name not in ingr_list:
                    ingr_list[ingredient_name] = {
                        'measure': measure,
                        'quantity': quantity
                    }
                else:
                    ingr_list[ingredient_name]['quantity'] += quantity
        else:
            print(f'Блюдо "{dish}" отсутствует в книге рецептов.')
    return ingr_list

def rewrite_file(file_paths):
    files_data = []
    
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            files_data.append((path, len(lines), lines))
    
    # Сортируем по количеству строк
    files_data.sort(key=lambda x: x[1])
    
    with open('combined_file.txt', 'w', encoding='utf-8') as f_total:
        for file_name, line_count, lines in files_data:
            f_total.write(f'--- Содержимое файла: {file_name} ---\n')
            f_total.write(f'Количество строк: {line_count}\n')
            f_total.writelines(lines)
            f_total.write('\n\n')  # Две пустые строки между файлами

if __name__ == '__main__':
    filename = "recipes.txt"
    cook_book = cook_book_from_file(path=filename)
    
    print('Книга рецептов:')
    for dish, ingredients in cook_book.items():
        print(f'Рецепт: {dish}')
        for ingredient in ingredients:
            print(f"{ingredient['ingredient_name']}: {ingredient['quantity']} {ingredient['measure']}")
        print()  # Пустая строка между рецептами
    
    print('Список покупок для блюд:')
    shop_list = get_shop_list_by_dishes(cook_book, dishes=['Запеченный картофель', 'Омлет'], person_count=2)
    pprint(shop_list)

    print('Объединение файлов:')
    rewrite_file(['1.txt', '2.txt', '3.txt'])
