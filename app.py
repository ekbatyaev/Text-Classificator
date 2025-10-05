import re
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from check_swear import SwearingCheck
from natasha import Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger

app = FastAPI()

API_TOKEN = ""

MODEL_PATH = "e5_large_finetuned_educational_process_second"
model = SentenceTransformer(MODEL_PATH)

# Цензор
segmenter = Segmenter()
morph_vocab = MorphVocab()
embedding = NewsEmbedding()
morph_tagger = NewsMorphTagger(embedding)
sch = SwearingCheck()

class TextRequest(BaseModel):
    text: str

categories = [
    "Учебный процесс", "Безопасность", "Наука", "Практическая подготовка",
    "Перемещения студентов / Изменения статусов студентов", "ГИА",
    "Траектории обучения", "Английский язык", "Цифровые компетенции",
    "Онлайн-обучение", "Дополнительное образование", "ОВЗ", "Выпускникам",
    "ВУЦ", "Внеучебка", "Социальные вопросы", "Общежития", "Цифровые системы",
    "Деньги", "Обратная связь"
]

ALCOHOL_WORDS = {
        "пиво", "водка", "вино", "коньяк", "шампанское",
        "ром", "джин", "виски", "текила", "ликер", "самогон"
    }


# Предподсчёт эмбеддингов категорий
cat_embeddings = model.encode(categories, convert_to_tensor=True, normalize_embeddings=True)

async def normalize(word: str) -> str:
    """Приводим слово к нормальной форме через Natasha"""
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        return token.lemma  # вернёт первую нормальную форму
    return word

async def detect_inappropriate(question: str) -> bool:
    # проверка на мат (через check-swear)
    # свой словарь алкоголя
    has_bad_words = sch.predict(question)
    # проверка на алкоголь (через словарь)
    # 2️⃣ Извлекаем все слова и нормализуем
    words = re.findall(r"\b[а-яё]+\b", question.lower())
    normalized_words = {await normalize(w) for w in words}
    alcohol_found = list(normalized_words & ALCOHOL_WORDS)
    if alcohol_found or has_bad_words[-1]:
        return True
    return False

def verify_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

@app.post("/predict")
async def predict(request: TextRequest, token: str = Depends(verify_token)):
    # Код предсказания
    q_emb = model.encode(request.text, convert_to_tensor=True, normalize_embeddings=True)
    cos_scores = util.cos_sim(q_emb, cat_embeddings)[0]

    best_idx = cos_scores.argmax().item()
    predicted_category = categories[best_idx]
    confidence = cos_scores[best_idx].item()
    bad = await detect_inappropriate(request.text)
    if bad:
        predicted_category = 0.0
    return {
        "question": request.text,
        "predicted_category": predicted_category,
        "confidence": float(confidence)
    }