from fastembed import TextEmbedding

# paraphrase-multilingual-MiniLM-L12-v2 — разновидность SBERT. Она отображает предложения и абзацы в 384-мерное векторное пространство и может быть использована для таких задач, как кластеризация или семантический поиск. Сам SBERT представляет собой модификацию BERT(LaBSE), оптимизированную для создания векторных представлений предложений и документов.

# Sentence-BERT(SBERT) модификация предварительно обученной сети BERT, которая использует сиамские и триплетные сетевые структуры для получения семантически значимых вкраплений предложений, которые можно сравнивать с помощью косинуса подобия. Это позволяет сократить время поиска наиболее похожей пары с 65 часов при использовании BERT / RoBERTa до примерно 5 секунд при использовании SBERT, сохраняя при этом точность BERT.


class BertEncoder:
    _instance: "BertEncoder | None" = None

    def __init__(self) -> None:
        self._model = TextEmbedding(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            max_length=512,
        )

    def encode(self, text: str) -> list[float]:
        vec = next(self._model.embed([text]))
        # @ - векторное произведение. Благодаря нормировке на единичную длину,
        # скалярное произведение эквивалентно косинусной мере.
        return (vec / (vec @ vec) ** 0.5).tolist()

    @classmethod
    def get_instance(cls) -> "BertEncoder":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
