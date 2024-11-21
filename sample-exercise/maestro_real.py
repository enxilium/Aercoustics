import os
import random
import librosa
import numpy as np
import pandas as pd
import soundfile as sf
import shutil
from glob import glob
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
LABEL_ROOT = os.path.join(DATA_DIR, "development_annotation")
INPUT_DIR = os.path.join(DATA_DIR, "development_audio")
random.seed(420)


def make_chunks(file_path, output_dir, chunk_duration=10):
    """
    Breaking down the audios into smaller chunks that are easier and more
    similar to our eventual data.
    """
    os.makedirs(output_dir, exist_ok=True)
    y, sr = librosa.load(file_path, sr=None)
    chunk_length = chunk_duration*sr
    chunks = [y[i:i + chunk_length] for i in range(0, len(y), chunk_length)]

    if len(chunks[-1]) < chunk_length:
        padding_length = chunk_length - len(chunks[-1])
        padding = np.random.normal(0, 0.01, padding_length)
        chunks[-1] = np.concatenate([chunks[-1], padding])

    chunk_paths = []
    for idx, chunk in enumerate(chunks):
        
        chunk_id = f"{os.path.basename(file_path).split('.')[0]}_chunk{idx}"
        output_path = os.path.join(output_dir, f"{chunk_id}.wav")
        sf.write(output_path, chunk, sr)
        chunk_paths.append((chunk_id, output_path, idx*chunk_duration,
                            (idx+1) * chunk_duration))

    return chunk_paths, sr


def process_labels_for_chunks(label_df, chunk_paths, all_labels, output_dir):
    """
    Labels for the chunks
    """
    for chunk_id, _, start_time, end_time in chunk_paths:
        chunk_events = label_df[(label_df["start_time"] < end_time) &
                                (label_df["end_time"] > start_time)]
        matrix = pd.DataFrame(columns=all_labels,
                              dtype=float)
        for _, row in chunk_events.iterrows():
            matrix.loc[row["start_time"],
                       row["sound_event"]] = row["uncertainty"]
            matrix = matrix.fillna(0.0)

        filepath = os.path.join(output_dir, f"{chunk_id}.csv")
        matrix.to_csv(filepath)


def process_audio_and_labels(input_dir, label_root, output_dir,
                             chunk_duration=10):
    """
    Everything put together.
    """
    os.makedirs(output_dir, exist_ok=True)
    train_dir = os.path.join(output_dir, "train")
    test_dir = os.path.join(output_dir, "test")
    validation_dir = os.path.join(output_dir, "validation")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(validation_dir, exist_ok=True)

    all_files = glob(os.path.join(label_root, "**", "*.txt"), recursive=True)
    all_labels = set()
    label_data = {}
    for file in all_files:
        file_df = pd.read_csv(file, sep="\t", header=None)

        file_df = file_df.rename(columns={0: "start_time",
                                          1: "end_time",
                                          2: "sound_event",
                                          3: "uncertainty"})
        label_data[file] = file_df
        all_labels.update(file_df["sound_event"])
    all_labels = sorted(list(all_labels))
    scenes = [d for d in os.listdir(input_dir)
              if os.path.isdir(os.path.join(input_dir, d))]
    train_set = []
    test_set = []

    for scene in scenes:
        scene_dir = os.path.join(input_dir, scene)
        files = [os.path.join(scene_dir, f)
                 for f in os.listdir(os.path.join(scene_dir))
                 if f.endswith(".wav")]
        test_file = random.choice(files)
        test_set.append((scene, test_file))
        train_files = [f for f in files if f != test_file]
        train_set.extend([(scene, f) for f in train_files])

    for scene, train_file in tqdm(train_set, desc="Processing train files"):
        chunk_paths, _ = make_chunks(train_file, train_dir, chunk_duration)
        label_file = os.path.join(label_root,
                                  f"soft_labels_{scene}",
                                  f"{os.path.basename(train_file).replace('.wav', '.txt')}")
        label_df = label_data[label_file]
        process_labels_for_chunks(label_df,
                                  chunk_paths,
                                  all_labels,
                                  output_dir=train_dir)

    for scene, test_file in tqdm(test_set, "Processing test file"):
        chunk_paths, _ = make_chunks(test_file, test_dir, chunk_duration)
        label_file = os.path.join(label_root,
                                  f"soft_labels_{scene}",
                                  f"{os.path.basename(test_file).replace('.wav','.txt')}")
        if label_file in label_data:
            label_df = label_data[label_file]
            process_labels_for_chunks(label_df,
                                      chunk_paths,
                                      all_labels,
                                      output_dir=test_dir)

    validation_set = random.sample(glob(os.path.join(train_dir, "**", "*.wav"),
                                        recursive=True), 75)
    for file in validation_set:
        label_file = file.replace('.wav', '.csv')
        shutil.move(file, validation_dir)
        shutil.move(label_file, validation_dir)


process_audio_and_labels(
    input_dir=INPUT_DIR,
    label_root=LABEL_ROOT,
    output_dir=os.path.join(DATA_DIR, "processed_data"),
    chunk_duration=10
)