from PIL import Image
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("facebook/nougat-base")
model = AutoModel.from_pretrained("facebook/nougat-base")



def image_to_markdown(image: Image):
    """Converts an image to markdown"""
    tokenized = tokenizer(image, return_tensors="pt")