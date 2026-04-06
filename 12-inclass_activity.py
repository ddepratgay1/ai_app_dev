from transformers import pipeline

model = pipeline("sentiment-analysis")
text = "This is the most straightforward and effective method I have ever learned"
result = model(text)
print(result)



