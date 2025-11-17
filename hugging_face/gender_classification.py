from transformers import pipeline

pipe = pipeline("image-classification", model="rizvandwiki/gender-classification-2")
pipe("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/hub/parrots.png")