import os
import random
import string
from timeit import default_timer as timer

# Функція побудови таблиці зсувів для алгоритму Boyer-Moore
def build_shift_table(pattern):
    table = {char: len(pattern) - index - 1 for index, char in enumerate(pattern[:-1])}
    table.setdefault(pattern[-1], len(pattern))
    return table

# Алгоритм Boyer-Moore
def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# Алгоритм KMP
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length, i = 0, 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    return lps

def kmp_search(text, pattern):
    lps, i, j = compute_lps(pattern), 0, 0
    while i < len(text):
        if pattern[j] == text[i]:
            i, j = i + 1, j + 1
        elif j:
            j = lps[j - 1]
        else:
            i += 1
        if j == len(pattern):
            return i - j
    return -1

# Алгоритм Rabin-Karp
def polynomial_hash(s, base=256, modulus=101):
    return sum((ord(c) * pow(base, len(s)-1-i, modulus)) % modulus for i, c in enumerate(s)) % modulus

def rabin_karp_search(text, pattern):
    pattern_length, text_length = len(pattern), len(text)
    pattern_hash = polynomial_hash(pattern)
    text_hash = polynomial_hash(text[:pattern_length])
    h_multiplier = pow(256, pattern_length - 1, 101)
    
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == text_hash and text[i:i+pattern_length] == pattern:
            return i
        if i < text_length - pattern_length:
            text_hash = (text_hash - ord(text[i]) * h_multiplier) * 256 + ord(text[i + pattern_length])
            text_hash %= 101
    return -1

# Функція для вимірювання часу виконання пошуку
def time_search(search_func, text, pattern):
    start = timer()
    result = search_func(text, pattern)
    end = timer()
    return end - start, result

# Функція для виконання тестів для заданого тексту та шаблонів
def run_tests(text, existing_pattern, non_existing_pattern):
    algorithms = [
        ("Boyer-Moore", boyer_moore_search),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp_search)
    ]
    return {name: (
        time_search(func, text, existing_pattern)[0],
        time_search(func, text, non_existing_pattern)[0]
    ) for name, func in algorithms}

# Читання файлу
def read_file(filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            return file.read()

# Функція для отримання випадкових підстрічок
def get_random_substring(text, length=10):
    return text[random.randint(0, len(text) - length):][:length]

def get_non_existing_substring(text, length=10):
    while True:
        non_existing = ''.join(random.choices(string.ascii_lowercase, k=length))
        if non_existing not in text:
            return non_existing

# Виведення таблиці з результатами
def print_table(results, article_num):
    print(f"\nРезультати для Статті {article_num}:")
    print(f"{'Алгоритм':<15}{'Час (Існуючий) (с)':<25}{'Час (Неіснуючий) (с)'}")
    print("-" * 60)
    for algo, (time_existing, time_non_existing) in results.items():
        print(f"{algo:<15}{time_existing:<25.6f}{time_non_existing:<25.6f}")

# Визначення найшвидшого алгоритму
def fastest_algo(results, pattern_type='existing'):
    return min(results, key=lambda x: results[x][0] if pattern_type == 'existing' else results[x][1])

if __name__ == "__main__":
    # Читання файлів
    article1 = read_file("article1.txt")
    article2 = read_file("article2.txt")

    # Отримання випадкових підстрічок
    existing_pattern_1, non_existing_pattern_1 = get_random_substring(article1), get_non_existing_substring(article1)
    existing_pattern_2, non_existing_pattern_2 = get_random_substring(article2), get_non_existing_substring(article2)

    # Запуск тестів для обох статей
    results_1, results_2 = run_tests(article1, existing_pattern_1, non_existing_pattern_1), run_tests(article2, existing_pattern_2, non_existing_pattern_2)

    # Виведення результатів у таблицю
    print_table(results_1, 1)
    print_table(results_2, 2)

    # Визначення найшвидших алгоритмів для існуючих та неіснуючих патернів
    print("\nВисновки:")
    print(f"Найшвидший алгоритм для Статті 1 (Існуючий патерн): {fastest_algo(results_1)}")
    print(f"Найшвидший алгоритм для Статті 1 (Неіснуючий патерн): {fastest_algo(results_1, 'non_existing')}")
    print(f"Найшвидший алгоритм для Статті 2 (Існуючий патерн): {fastest_algo(results_2)}")
    print(f"Найшвидший алгоритм для Статті 2 (Неіснуючий патерн): {fastest_algo(results_2, 'non_existing')}")

    # Визначення загального найшвидшого алгоритму для існуючого та неіснуючого патернів
    all_results = {**results_1, **results_2}
    print(f"Загальний найшвидший алгоритм для Існуючого патерну: {fastest_algo(all_results)}")
    print(f"Загальний найшвидший алгоритм для Неіснуючого патерну: {fastest_algo(all_results, 'non_existing')}")