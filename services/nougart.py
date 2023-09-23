from PIL import Image
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("facebook/nougat-base")
model = AutoModel.from_pretrained("facebook/nougat-base")



def image_to_markdown(image: Image):
    """Converts an image to markdown"""
    tokenized = tokenizer(image, return_tensors="pt")

def query_hugginface_inference_api(payload, model_dir):
    query_count = 0
    token = os.environ.get("HF_API_TOKEN")
    url = "https://api-inference.huggingface.co/models/" + model_dir
    data = payload
    if isinstance(payload, dict):
        data = json.dumps(payload)
    headers = {"Authorization": f"Bearer {token}"}

    def _query(url, headers, data):
        nonlocal query_count
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        if "error" in data:
            if data["error"] == "Model not found":
                raise ValueError(f"Model {model_dir} not found")
            elif data["error"] == f"Model {model_dir} is currently loading":
                time.sleep(int(data["estimated_time"]))
                if query_count < 3:
                    query_count += 1
                    return _query(url, headers, data)
                else:
                    raise ValueError("Issue loading the model, recurssion max depth exceeded")
            else:
                return data
        return data

    return _query(url, headers, data)

