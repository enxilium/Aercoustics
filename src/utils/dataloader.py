import torch
from torch.utils.data import DataLoader, Dataset


# Custom dataset
class AudioTextDataset(Dataset):
    def __init__(self, audio_inputs, text_inputs, labels):
        self.audio_inputs = audio_inputs
        self.text_inputs = text_inputs
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.audio_inputs[idx], self.text_inputs[idx], self.labels[idx]

# Collate function for DataLoader
def collate_fn(batch):
    audio_inputs, text_inputs, labels = zip(*batch)
    
    # Process audio inputs
    audio_features = [item['input_features'] for item in audio_inputs]
    audio_features = torch.cat(audio_features, dim=0)
    
    # Process text inputs
    text_input_ids = [item['input_ids'].squeeze() for item in text_inputs]
    text_attention_mask = [item['attention_mask'].squeeze() for item in text_inputs]
    
    # Pad text inputs
    max_len = max(len(ids) for ids in text_input_ids)
    text_input_ids = [torch.nn.functional.pad(ids, (0, max_len - len(ids))) for ids in text_input_ids]
    text_attention_mask = [torch.nn.functional.pad(mask, (0, max_len - len(mask))) for mask in text_attention_mask]
    
    text_input_ids = torch.stack(text_input_ids)
    text_attention_mask = torch.stack(text_attention_mask)
    
    labels = torch.stack(labels)
    
    return {
        'audio_inputs': {'input_features': audio_features},
        'text_inputs': {'input_ids': text_input_ids, 'attention_mask': text_attention_mask},
        'labels': labels
    }