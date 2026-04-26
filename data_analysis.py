import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def get_sessions(file_name: str):
    sessions = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if line:
                sessions.append(json.loads(line))
    return sessions


if __name__ == "__main__":
    sessions = get_sessions("sessions.jsonl")

    print(f"Всего сессий: {len(sessions)}")

    lengths = [len(s) for s in sessions]
    all_items = [item for session in sessions for item in session]
    unique_items = set(all_items)

    repeat_ratio = []
    for session in sessions:
        unique_in_session = len(set(session))
        repeat_ratio.append(1 - unique_in_session / len(session))

    max_repeats = []
    for session in sessions:
        item_counts = {}
        for item in session:
            item_counts[item] = item_counts.get(item, 0) + 1
        max_repeats.append(max(item_counts.values()))

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # График 1: Столбиковая диаграмма длин сессий
    length_counter = Counter(lengths)
    lengths_sorted = sorted(length_counter.items())
    x, y = zip(*lengths_sorted)

    axes[0, 0].bar(x, y, edgecolor='black')
    axes[0, 0].set_xlabel('Длина сессии')
    axes[0, 0].set_ylabel('Количество сессий')
    axes[0, 0].set_title('Распределение длин сессий')
    axes[0, 0].set_xticks(x)

    for i, v in enumerate(y):
        axes[0, 0].text(x[i], v + 0.1, str(v), ha='center', va='bottom', fontsize=8)

    # График 2: Топ-10 самых популярных товаров
    item_freq = {}
    for item in all_items:
        item_freq[item] = item_freq.get(item, 0) + 1

    top_items = sorted(item_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    top_ids, top_counts = zip(*top_items)

    axes[0, 1].bar(range(len(top_ids)), top_counts, edgecolor='black')
    axes[0, 1].set_xlabel('ID товара')
    axes[0, 1].set_ylabel('Частота')
    axes[0, 1].set_title('Топ-10 самых популярных товаров')
    axes[0, 1].set_xticks(range(len(top_ids)))
    axes[0, 1].set_xticklabels(top_ids)

    for i, v in enumerate(top_counts):
        axes[0, 1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=7)

    # График 3: Доля повторяющихся товаров
    repeat_counter = {}
    for ratio in repeat_ratio:
        bucket = round(ratio * 20) / 20
        repeat_counter[bucket] = repeat_counter.get(bucket, 0) + 1

    repeat_sorted = sorted(repeat_counter.items())
    x_rep, y_rep = zip(*repeat_sorted)

    axes[0, 2].bar(x_rep, y_rep, width=0.04, edgecolor='black')
    axes[0, 2].set_xlabel('Доля повторяющихся товаров в сессии')
    axes[0, 2].set_ylabel('Количество сессий')
    axes[0, 2].set_title('Повторяемость товаров внутри сессий')
    axes[0, 2].set_xticks(x_rep)
    axes[0, 2].set_xticklabels([f'{x:.2f}' for x in x_rep], rotation=45)

    for i, v in enumerate(y_rep):
        axes[0, 2].text(x_rep[i], v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    # График 4: Топ-10 товаров на первом месте в сессии
    first_items = [s[0] for s in sessions if s]

    first_freq = {}
    for item in first_items:
        first_freq[item] = first_freq.get(item, 0) + 1

    top_first = sorted(first_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    x_first, y_first = zip(*top_first)

    axes[1, 0].bar(range(len(x_first)), y_first, edgecolor='black')
    axes[1, 0].set_xlabel('ID товара')
    axes[1, 0].set_ylabel('Количество сессий')
    axes[1, 0].set_title('Топ-10 товаров на первом месте')
    axes[1, 0].set_xticks(range(len(x_first)))
    axes[1, 0].set_xticklabels(x_first)

    for i, v in enumerate(y_first):
        axes[1, 0].text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    # График 5: Топ-10 товаров на последнем месте в сессии
    last_items = [s[-1] for s in sessions if s]

    last_freq = {}
    for item in last_items:
        last_freq[item] = last_freq.get(item, 0) + 1

    top_last = sorted(last_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    x_last, y_last = zip(*top_last)

    axes[1, 1].bar(range(len(x_last)), y_last, edgecolor='black')
    axes[1, 1].set_xlabel('ID товара')
    axes[1, 1].set_ylabel('Количество сессий')
    axes[1, 1].set_title('Топ-10 товаров на последнем месте')
    axes[1, 1].set_xticks(range(len(x_last)))
    axes[1, 1].set_xticklabels(x_last)

    for i, v in enumerate(y_last):
        axes[1, 1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    # График 6: Максимальное количество повторений товара в одной сессии
    max_repeat_counter = {}
    for r in max_repeats:
        max_repeat_counter[r] = max_repeat_counter.get(r, 0) + 1

    max_repeat_sorted = sorted(max_repeat_counter.items())
    x_max, y_max = zip(*max_repeat_sorted)

    axes[1, 2].bar(x_max, y_max, edgecolor='black')
    axes[1, 2].set_xlabel('Максимальное количество повторов товара')
    axes[1, 2].set_ylabel('Количество сессий')
    axes[1, 2].set_title('Максимум повторов одного товара')
    axes[1, 2].set_xticks(x_max)

    for i, v in enumerate(y_max):
        axes[1, 2].text(x_max[i], v + 0.5, str(v), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()

    # Статистика по сессиям
    print(f"\nСтатистика длин сессий:")
    print(f"Минимальная длина: {min(lengths)}")
    print(f"Максимальная длина: {max(lengths)}")
    print(f"Средняя длина: {np.mean(lengths):.2f}")

    # Статистика по товарам
    print(f"\nСтатистика по товарам:")
    print(f"Всего просмотров: {len(all_items)}")
    print(f"Уникальных товаров: {len(unique_items)}")
    print(f"Средняя частота товара: {len(all_items) / len(unique_items):.2f}")

    # Поиск часто повторяющихся товаров
    repeat_items = Counter()
    for session in sessions:
        for item in set(session):
            count = session.count(item)
            if count >= 5:
                repeat_items[item] += 1

    if repeat_items:
        print(f"\nТовары, которые повторяются ≥5 раз в одной сессии:")
        for item, session_count in repeat_items.most_common(10):
            print(f"  Товар {item}: в {session_count} сессиях")
    else:
        print(f"\nАномально частых повторов не найдено")