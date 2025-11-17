# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

# text = "Ce produit est absolument fantastique ! Je l'adore."

# result = pipe(text)
# print(result)  

# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

model.summerize()
model.eval()

# inputs = tokenizer(text, return_tensors="pt")
# outputs = model(**inputs)

