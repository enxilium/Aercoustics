import os
import torch
from data_loader import SEDDataset
from utils import save_checkpoint, setup_logger
# Add the model and stuff

logger = setup_logger(log_dir="logs/")  # Remove if you are using notebooks

# Add your model, optimizers, crit, anything else that needs to be init

train_dataset = SEDDataset(data_dir=os.path.join("data", "processed_data",
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
