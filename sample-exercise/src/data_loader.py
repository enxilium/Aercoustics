import os
import librosa
import torch
import pandas as pd
from torch.utils.data import Dataset


class SEDDataset(Dataset):
    def __init__(self, data_dir):
        """
        Init the dataloader with labels.
        """
        self.audio_paths = []
        self.labels = []

        for file in os.listdir(data_dir):
            if file.endswith(".wav"):
                csv_file = file.replace(".wav", ".csv")
                audio_path = os.path.join(data_dir, file)
                csv_path = os.path.join(data_dir, csv_file)
                self.audio_paths.append(audio_path)
                self.labels.append(csv_path)

    def __len__(self):
        return len(self.audio_paths)

    def __getitem__(self, idx):
        """
        Load Audio and a given index
        """
        audio_path = self.audio_paths[idx]
        label_path = self.labels[idx]

        waveform, _ = librosa.load(audio_path, sr=None)
        waveform = torch.tensor(waveform).float

        labels = self._process_labels(label_path)

        return labels, waveform

    def _process_labels(self, label_path):
        """
        Label CSV to tensor
        """
        labels_df = pd.read_csv(label_path)
        labels_df = labels_df.drop(columns=['Unnamed: 0'], errors='ignore')
        labels_tensor = torch.tensor(labels_df.values).float()

        if labels_tensor.shape[0] < 10:
            padding = torch.zeros((10 - labels_tensor.shape[0]),
                                  labels_tensor.shape[1])
            labels_tensor = torch.cat([labels_tensor, padding], dim=0)

        return labels_tensor
