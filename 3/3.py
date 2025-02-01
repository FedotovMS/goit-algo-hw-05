import os
import random
import string
from timeit import default_timer as timer

# Функція побудови таблиці зсувів для алгоритму Boyer-Moore
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
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

# Функція обчислення масиву LPS для алгоритму KMP
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Алгоритм KMP
def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

# Поліноміальний хеш-функція для алгоритму Rabin-Karp
def polynomial_hash(s, base=256, modulus=101):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + ord(char)) % modulus
    return hash_value

# Алгоритм Rabin-Karp
def rabin_karp_search(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)
    base = 256
    modulus = 101

    pattern_hash = polynomial_hash(pattern, base, modulus)
    text_slice_hash = polynomial_hash(text[:pattern_length], base, modulus)

    h_multiplier = pow(base, pattern_length - 1) % modulus

    for i in range(text_length - pattern_length + 1):
        if pattern_hash == text_slice_hash:
            if text[i:i+pattern_length] == pattern:
                return i

        if i < text_length - pattern_length:
            text_slice_hash = (text_slice_hash - ord(text[i]) * h_multiplier) % modulus
            text_slice_hash = (text_slice_hash * base + ord(text[i + pattern_length])) % modulus
            if text_slice_hash < 0:
                text_slice_hash += modulus

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
    
    results = {}
    for name, func in algorithms:
        time_existing, _ = time_search(func, text, existing_pattern)
        time_non_existing, _ = time_search(func, text, non_existing_pattern)
        results[name] = (time_existing, time_non_existing)
    
    return results

# Читання файлу
def read_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Якщо UTF-8 не працює, пробуємо з іншою кодуванням
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            return file.read()

# Функція для отримання випадкової підстрічки з тексту
def get_random_substring(text, length=10):
    start = random.randint(0, len(text) - length)
    return text[start:start+length]

# Функція для отримання випадкової непідтвердженої підстрічки
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
    for algo, times in results.items():
        print(f"{algo:<15}{times[0]:<25.6f}{times[1]:<25.6f}")

# Функція для знаходження найшвидшого алгоритму
def fastest_algo(results):
    return min(results, key=lambda x: sum(results[x]))

if __name__ == "__main__":
    # Читання файлів
    article1 = read_file("article1.txt")
    article2 = read_file("article2.txt")

    # Отримання випадкових підстрічок
    existing_pattern_1 = get_random_substring(article1)
    non_existing_pattern_1 = get_non_existing_substring(article1)

    existing_pattern_2 = get_random_substring(article2)
    non_existing_pattern_2 = get_non_existing_substring(article2)

    # Запуск тестів для обох статей
    results_1 = run_tests(article1, existing_pattern_1, non_existing_pattern_1)
    results_2 = run_tests(article2, existing_pattern_2, non_existing_pattern_2)

    # Виведення результатів у таблицю
    print_table(results_1, 1)
    print_table(results_2, 2)

    # Визначення найшвидших алгоритмів для існуючих патернів
    fastest_existing_1 = fastest_algo({k: (v[0], 0) for k, v in results_1.items()})
    fastest_existing_2 = fastest_algo({k: (v[0], 0) for k, v in results_2.items()})

    # Визначення найшвидших алгоритмів для неіснуючих патернів
    fastest_non_existing_1 = fastest_algo({k: (0, v[1]) for k, v in results_1.items()})
    fastest_non_existing_2 = fastest_algo({k: (0, v[1]) for k, v in results_2.items()})

    # Виведення висновків
    print("\nВисновки:")
    print(f"Найшвидший алгоритм для Статті 1 (Існуючий патерн): {fastest_existing_1}")
    print(f"Найшвидший алгоритм для Статті 1 (Неіснуючий патерн): {fastest_non_existing_1}")
    print(f"Найшвидший алгоритм для Статті 2 (Існуючий патерн): {fastest_existing_2}")
    print(f"Найшвидший алгоритм для Статті 2 (Неіснуючий патерн): {fastest_non_existing_2}")

    # Визначення загального найшвидшого алгоритму для існуючого патерну
    fastest_overall_existing = fastest_algo({
        k: (v[0], 0) for k, v in {**results_1, **results_2}.items()
    })

    # Визначення загального найшвидшого алгоритму для неіснуючого патерну
    fastest_overall_non_existing = fastest_algo({
        k: (0, v[1]) for k, v in {**results_1, **results_2}.items()
    })

    print(f"Загальний найшвидший алгоритм для Існуючого патерну: {fastest_overall_existing}")
    print(f"Загальний найшвидший алгоритм для Неіснуючого патерну: {fastest_overall_non_existing}")