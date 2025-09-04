from random import randint
from collections import Counter

# Параметры для задания ключевой последовательности
L = 35
N = 200000

# Переменная для хранения ключевой последовательности
m = []

k = int(input("Введите k для сериального теста (2/3/4): "))
k2 = int(input("Введите k для корреляционного теста (1/2/8/9): "))
path_for_key = input("Введите путь к файлу для ключевой последовательности: ")


# Функция для генерации псевдослучайной последовательности
def generator_m():
    downl = input("Загрузить начальное состояние регистра из файла key.txt? [y/n]: ")
    if downl == "y":
        with open(path_for_key, "r", encoding="utf-8") as inp:
            start = list(map(int, inp.read()))

    else:
        start = [randint(0, 1) for _ in range(L)]
        with open(path_for_key, "w", encoding="utf-8") as out:
            out.write("".join(map(str, start)))

    for _ in range(N):
        # считаем левый бит по полиному
        left = start[34] ^ start[1]

        # бит, который выпадает, добавляем в последовательность
        m.append(start[-1])

        # смещаем все биты
        for i in range(len(start) - 1, 0, -1):
            start[i] = start[i - 1]

        start[0] = left  # посчитанный бит добавляем слева


# Функция для сериального теста
def serial(p, l):
    d = dict()
    for i in range(0, l, k):
        if i + k <= l:
            comb = "".join(map(str, p[i : i + k]))
            d[comb] = d.get(comb, 0) + 1
    N_teor = l / (k * (2**k))
    # print(f' dict: {d}')
    # print(f'teor {N_teor}')
    hi = 0
    for key in d:
        hi += ((d[key] - N_teor) ** 2) / N_teor
    if k == 2:
        hi_a_max = 0.584
        hi_a_min = 6.251
    elif k == 3:
        hi_a_max = 2.833
        hi_a_min = 12.017
    elif k == 4:
        hi_a_max = 8.547
        hi_a_min = 22.307

    print(f"Критерий Пирсона для сериального теста = {hi}")
    if hi_a_max <= hi <= hi_a_min:
        print("Сериальный тест пройден")
    else:
        print("Сериальный тест провален")


# Функция для корреляционного теста
def korrl(p, k2, l):
    mi = 1 / (l - k2) * sum(p[i] for i in range(0, l - k2))
    mik = 1 / (l - k2) * sum(p[i] for i in range(k2, l))

    dxi = 1 / (l - k2 - 1) * sum((p[i] - mi) ** 2 for i in range(0, l - k2))
    dxik = 1 / (l - k2 - 1) * sum((p[i] - mik) ** 2 for i in range(k2, l))

    r = (
        1
        / (l - k2)
        * sum((p[i] - mi) * (p[i + k2] - mik) for i in range(0, l - k2))
        / (dxi * dxik) ** 0.5
    )
    rkr = 1 / (l - 1) + 2 / (l - 2) * ((l * (l - 3)) / (l + 1)) ** 0.5
    print(f"R[{k2}] = {r}")
    if abs(r) <= rkr:
        print("Корреляционный тест пройден")
    else:
        print("Корреляционный тест провален")


# Функция для покер-теста
def poker(p, l):
    x = [int("".join(map(str, p[i : i + 32])), 2) for i in range(0, l, 32)]
    r = [el / ((2**32) - 1) for el in x]
    u = [int(el * 10) for el in r]
    qvint = [u[i : i + 5] for i in range(0, len(u), 5)]
    q_vse, q_tetr, q_tri_dupl, q_tri, q_2dupl, q_dupl, q = 0, 0, 0, 0, 0, 0, 0
    for pt in qvint:
        val = list(Counter(pt).values())
        if 5 in val:
            q_vse += 1
        elif 4 in val:
            q_tetr += 1
        elif 3 in val and 2 in val:
            q_tri_dupl += 1
        elif 3 in val and 1 in val:
            q_tri += 1
        elif val.count(2) == 2:
            q_2dupl += 1
        elif val.count(1) == 3:
            q_dupl += 1
        else:
            q += 1

    q_vse /= l / 160
    q_tetr /= l / 160
    q_tri_dupl /= l / 160
    q_tri /= l / 160
    q_2dupl /= l / 160
    q_dupl /= l / 160
    q /= l / 160

    p1 = 9 * 8 * 7 * 6 / 10**4
    p2 = 9 * 8 * 7 / 10**3
    p3 = 15 * 9 * 8 / 10**4
    p4 = 9 * 8 / 10**3
    p5 = 9 / 10**3
    p6 = 5 * 9 / 10**4
    p7 = 1 / 10**4

    n1 = ((q - p1) ** 2) / p1
    n2 = ((q_dupl - p2) ** 2) / p2
    n3 = ((q_2dupl - p3) ** 2) / p3
    n4 = ((q_tri - p4) ** 2) / p4
    n5 = ((q_tri_dupl - p5) ** 2) / p5
    n6 = ((q_tetr - p6) ** 2) / p6
    n7 = ((q_vse - p7) ** 2) / p7

    hi = n1 + n2 + n3 + n4 + n5 + n6 + n7

    print(f"Критерий Пирсона для покер-теста = {hi}")
    if 2.2 <= hi <= 10.64:
        print("Покер-тест пройден")
    else:
        print("Покер-тест провален")


# Функция для шифрования/дешифрования текста
def encrypt_decrypt(inp, out, k):
    with open(inp, "r", encoding="utf-8") as txt:
        text = ""
        i = 0
        for el in txt.read():
            M = "".join(map(str, k[i : i + 8]))
            i += 8
            text += chr(ord(el) ^ int(M, 2))

    with open(out, "w", encoding="utf-8") as output:
        output.write(text)


# Функция для приведение текста в бинарный формат
def bintext(filename):
    s = ""
    with open(filename, "r", encoding="utf-8") as txt:
        for el in txt.read():
            s += format(ord(el), "b")
    s1 = list(map(int, s))
    return s, s1


generator_m()
for i in range(0, 50):
    print(m[i], end=", ")

print("Тесты для М-последовательности: ")
serial(m, N)
korrl(m, k2, N)
poker(m, N)


text = input("Укажите путь к файлу, который надо зашифровать: ")
encrypted_text = input("Путь к файлу, куда записать шифр: ")
decrypted_text = input("Путь к файлу, куда записать расшифрованный текст: ")

encrypt_decrypt(text, encrypted_text, m)
encrypt_decrypt(encrypted_text, decrypted_text, m)

# Для исследования двоичного предствления исходного и зашифрованного текста
s, s1 = bintext(text)
s3, s4 = bintext(encrypted_text)

print("Тесты для исходного текста: ")
serial(s, len(s))
korrl(s1, k2, len(s1))
poker(s, len(s))

print("Тесты для зашифрованного текста: ")
serial(s3, len(s3))
korrl(s4, k2, len(s4))
poker(s3, len(s3))

# Исследование уменьшения ключевой последовательности
key = m[:8] * len(s)
encrypted_new = input(
    "Укажите путь для файла, куда будет записываться новый шифр, для меньшего ключа: "
)
encrypt_decrypt(text, encrypted_new, key)
t, t1 = bintext(encrypted_new)

# Расчет значение корреляционной функции для нового шифра
for k2 in range(0, 17):
    korrl(t1, k2, len(t1))
