import os
import torch
import torch.nn as nn
from data_loader import SEDDataset
from utils import save_checkpoint, setup_logger
from torchvision.models import resnet50
from torchvision import models
# Add the model and stuff

logger = setup_logger(log_dir="logs/")  # Remove if you are using notebooks

# Add your model, optimizers, crit, anything else that needs to be init

train_dataset = SEDDataset(data_dir=os.path.join("sample-exercise", "data", "processed_data", # Output shape: 10 x 17. 17 classes across ten seconds going down.
                                                 "train"))

train_loader = torch.utils.data.DataLoader(train_dataset, shuffle=True,
                                           batch_size=16)
# Change batch_size

def train(model, train_loader, optimizer, criterion, num_epochs,
          checkpoint_dir):
    # Change to match your training loop
    # Or just do it on notebooks whatever works for you
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for waveform, labels in train_loader:
            optimizer.zero_grad()

            outputs = model(waveform)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(train_loader)
        logger.info(f"Epoch {epoch + 1}{num_epochs}, Loss: {avg_loss:.4f}")
        save_checkpoint({'model_state': model.state_dict(),
                         'optimizer_state': optimizer.state_dict()},
                        checkpoint_dir)


checkpoint_dir = "../checkpoints/"

class AudioClassifier(nn.Module):
    def __init__(self, num_labels, num_segments): # Number of classes, number of time segments
        super().__init__()
        self.res_net = models.resnet50(pretrained=True)

        self.res_net.fc = nn.Identity() # Get rid of the old fc layer

        self.classifier = nn.Sequential(
            nn.Linear(2048, 512), # Output of last conv layer of resnet is 2048
            nn.ReLU(), # Apply non-linearity element-wise
            nn.Linear(512, num_segments * num_labels) # Output layer
        )
    
    def forward(self, x):
        features = self.res_net(x) # Output of res_net from spectrogram

        output = self.classifier(features)


model = AudioClassifier(num_labels=17, num_segments=10) # 17 classes, 10 time segments
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

train(model, train_loader, optimizer, criterion, num_epochs=10, checkpoint_dir=checkpoint_dir)



