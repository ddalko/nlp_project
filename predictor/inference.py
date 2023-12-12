import torch
from openai import OpenAI
client = OpenAI()

from predictor.model import NeuralNet
best_model = NeuralNet()
best_model.load_state_dict(torch.load('/Users/dk/Desktop/Desktop/nlp_project/predictor/best_model.pth'))
best_model.eval()

def inference(inp: str):
    response = client.embeddings.create(
        input=inp,
        model="text-embedding-ada-002",
    )
    print(response)
    vector = response.data[0].embedding
    x = torch.tensor(vector, dtype=torch.float)
    return best_model.inference(x)