import os
import torch
import logging


def save_checkpoint(state, checkpoint_dir, filename="checkpoint.pth.tar"):
    os.makedirs(checkpoint_dir, exist_ok=True)
    file_path = os.path.join(checkpoint_dir, filename)
    torch.save(state, file_path)

    print(f"checkpointed to {file_path}")


def load_checkpoint(checkpoint_path, model, optimizer=None):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state'])
    if optimizer:
        optimizer.load_state_dict(checkpoint["optimizer_state"])
    print("Got Checkpoint")


def setup_logger(log_dir, log_file="train.log"):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        # Change this if required
                        handlers=[
                            logging.FileHandler(log_path),
                            logging.StreamHandler()
                            ]
                        )
    return logging.getLogger()
