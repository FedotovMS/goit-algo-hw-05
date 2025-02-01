def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return (iterations, arr[mid])  # Якщо точний елемент знайдений
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    """ Якщо точний елемент не знайдений, то upper_bound - це перший елемент,
        що більший або рівний target"""
    if left < len(arr):   
        upper_bound = arr[left]
    return (iterations, upper_bound)

# Тестуємо функцію:
arr = [1.2, 2.5, 3.7, 4.1, 5.6, 6.8]
target = 4.0

result = binary_search(arr, target)
print(result)  # Виведе кількість ітерацій і верхню межу