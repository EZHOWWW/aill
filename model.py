from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch



sentiment = float


class SentimentAnalyzer:
    def __init__(self):
        self.model_checkpoint = "cointegrated/rubert-tiny-sentiment-balanced"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_checkpoint
        )

    def predict(self, text: str) -> sentiment:
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            logits = self.model(**inputs).logits
        proba = torch.sigmoid(logits).cpu().numpy()[0]
        return proba.dot([-1, 0, 1])  # Оценка от -1 (негатив) до 1 (позитив)
