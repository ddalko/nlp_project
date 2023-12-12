# !pip install pandas
# !pip install openai
# !pip install scikit-learn
# !pip install torch

import json
import glob

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class TextEmbeddingDataset(Dataset):
    def __init__(self, data_root_dir: str):
        # Load data from dir
        self.data = []
        for json_path in sorted(glob.glob(f"{data_root_dir}/*.json")):
          with open(json_path, 'r') as jfd:
            json_data = json.load(jfd)
            self.data.append({
                "embedding": json_data["result"]["data"][0]["embedding"],
                "score": json_data["score"],
                "raw_data": json_data["raw_data"],
            })

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        embedding = self.data[idx]['embedding']
        score = self.data[idx]['score']
        raw_data = self.data[idx]['raw_data']
        return {
            'embedding': torch.tensor(embedding, dtype=torch.float),
            'score': torch.tensor(score, dtype=torch.float),
            'raw_data': raw_data,
        }


class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(1536, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def inference(self, vector: torch.Tensor):
        outputs = self.forward(vector).squeeze()
        score = torch.clamp(outputs, min=0.0, max=5.0).round()
        return int(score.item())

    
def main():
    val_dataset = TextEmbeddingDataset("./val")
    val_data_loader = DataLoader(val_dataset, batch_size=32, shuffle=True)

    best_model = NeuralNet()
    best_model.load_state_dict(torch.load('best_model.pth'))
    best_model.eval()

    correct, total = 0, 0
    with torch.no_grad():
        for data in val_data_loader:
            embeddings = data['embedding']
            scores = data['score']

            outputs = best_model(embeddings).squeeze()
            predicted = torch.clamp(outputs, min=0.0, max=5.0).round()

            for idx, elem in enumerate(zip(scores, outputs)):
                score, predicted_score = elem          
                print('\n'.join([f"{k}: {data['raw_data'][k][idx]}" for k in data['raw_data'].keys() if type(data['raw_data'][k][idx]) == str]))
                print(f"predicted score: {predicted_score}")
                print(f"GT score: {score}")

                total += scores.size(0)
                correct += (predicted == scores).sum().item()

    accuracy = correct / total
    print(f'Accuracy: {accuracy:.4f}')

if __name__ == "__main__":
    main()