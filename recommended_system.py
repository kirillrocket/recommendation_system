from typing import List, Dict, Tuple
from collections import defaultdict
from data_analysis import get_sessions


class Recommendations:
    def __init__(self, sessions_file: str = "sessions.jsonl", smoothing: float = 0.001):
        self.sessions: List[List[int]] = get_sessions(sessions_file)
        self.smoothing: float = smoothing
        self.train_sessions: List[List[int]] = []
        self.test_targets: List[int] = []
        self.transitions: Dict[int, Dict[int, int]] = {}
        self.probabilities: Dict[int, Dict[int, float]] = {}
        self.popular_items: List[int] = []

    # ШАГ 02
    def train_test_split(self) -> Tuple[List[List[int]], List[int]]:
        self.train_sessions = [session[:-1] for session in self.sessions]
        self.test_targets = [session[-1] for session in self.sessions]
        return self.train_sessions, self.test_targets

    # ШАГ 03
    def build_graph(self) -> Dict[int, Dict[int, int]]:
        transitions = defaultdict(lambda: defaultdict(int))

        for session in self.train_sessions:
            for i in range(len(session) - 1):
                transitions[session[i]][session[i + 1]] += 1

        self.transitions = {item: dict(next_items) for item, next_items in transitions.items()}
        return self.transitions

    def get_probabilities(self) -> Dict[int, Dict[int, float]]:
        self.probabilities = {}

        for item, next_items in self.transitions.items():
            total = sum(next_items.values())
            num_transitions = len(next_items)

            probs_for_item = {}
            for next_item, count in next_items.items():
                smoothed_count = count + self.smoothing
                smoothed_total = total + self.smoothing * num_transitions
                probs_for_item[next_item] = smoothed_count / smoothed_total

            self.probabilities[item] = probs_for_item

        return self.probabilities

    def get_popular_items(self, top_n: int = 10) -> List[int]:
        """Вычисление топ-N популярных товаров."""
        freq = defaultdict(int)
        for session in self.train_sessions:
            for item in session:
                freq[item] += 1

        sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        self.popular_items = [item for item, _ in sorted_items[:top_n]]
        return self.popular_items

    # ШАГ 04
    def recommend(self, last_item: int, n_recommendations: int = 10) -> List[int]:
        """
        Рекомендации на основе последнего товара.
        Если товар не встречался — возвращает популярные товары.
        """
        if last_item not in self.probabilities:
            return self.popular_items[:n_recommendations]

        sorted_transitions = dict(sorted(self.probabilities[last_item].items(), key=lambda x: x[1], reverse=True))

        recommendations = [item for item in sorted_transitions.keys() if item != last_item][:n_recommendations]

        if len(recommendations) < n_recommendations:
            for popular_item in self.popular_items:
                if popular_item not in recommendations and popular_item != last_item:
                    recommendations.append(popular_item)
                    if len(recommendations) == n_recommendations:
                        break

        return recommendations

    def get_all_recommendations(self, n_recommendations: int = 10) -> List[List[int]]:
        all_recommendations = []

        for session in self.train_sessions:
            if not session:
                all_recommendations.append(self.popular_items[:n_recommendations])
            else:
                last_item = session[-1]
                recs = self.recommend(last_item, n_recommendations)
                all_recommendations.append(recs)

        return all_recommendations

    # ШАГ 05
    def hit_at_k(self, recommendations: List[List[int]], k: int = 10) -> float:
        assert len(recommendations) == len(self.test_targets)

        hits = 0
        for recs, true_item in zip(recommendations, self.test_targets):
            if true_item in recs[:k]:
                hits += 1

        return hits / len(self.test_targets)

    def baseline_recommendations(self, n_recommendations: int = 10) -> List[List[int]]:
        return [self.popular_items[:n_recommendations] for _ in self.train_sessions]

    def evaluate(self, k: int = 10) -> None:
        """Оценка модели и сравнение с бейзлайном."""
        # Рекомендации модели
        model_recs = self.get_all_recommendations(k)
        model_hit = self.hit_at_k(model_recs, k)

        # Рекомендации бейзлайна
        baseline_recs = self.baseline_recommendations(k)
        baseline_hit = self.hit_at_k(baseline_recs, k)

        print(f"\nHit@{k} модели: {model_hit:.4f} ({model_hit * 100:.2f}%)")
        print(f"Hit@{k} бейзлайна: {baseline_hit:.4f} ({baseline_hit * 100:.2f}%)")
        print(f"Разница: {model_hit - baseline_hit:+.4f}")

        if model_hit > baseline_hit:
            print(f"\nМодель обходит бейзлайн")
        elif model_hit < baseline_hit:
            print(f"\nМодель уступает бейзлайну")
        else:
            print(f"\nМодели показывают одинаковый результат")

    def run(self) -> None:
        # ШАГ 02
        self.train_test_split()
        print(f"Обучающих сессий: {len(self.train_sessions)}")

        # ШАГ 03
        self.build_graph()
        self.get_probabilities()
        self.get_popular_items()

        # ШАГ 05
        self.evaluate()


def main():
    model = Recommendations(sessions_file="sessions.jsonl")
    model.run()


if __name__ == "__main__":
    main()