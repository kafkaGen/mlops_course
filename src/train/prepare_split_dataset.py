import argparse
import json
import os

import pandas as pd
from sklearn.model_selection import train_test_split


def load_dataset(dataset_json_path: str) -> pd.DataFrame:
    dataset = []

    with open(dataset_json_path) as jf:
        data = json.load(jf)

    for item in data:
        dataset.append(
            {
                "prompt": item["data"]["text"],
                "label": item["annotations"][0]["result"][0]["value"]["choices"][0],
            }
        )

    print("Dataset loaded.")

    return pd.DataFrame(dataset)


def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df["prompt"] = df["prompt"].str.strip().str.lower()
    df["prompt"] = df["prompt"].str.replace(r"[^\w\s]", "", regex=True)
    df["prompt"] = df["prompt"].str.replace(r"\s+", " ", regex=True).str.strip()
    return df


def split_dataset(df: pd.DataFrame, test_size: float, seed: int = 13) -> tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=test_size, random_state=seed)

    print(f'Train dataset size: {len(train)}, Injection proportion: {train["label"].value_counts()["Injection"] / len(train)}.')
    print(f'Test dataset size: {len(test)}, Injection proportion: {test["label"].value_counts()["Injection"] / len(test)}.')

    return train, test


def save_fasttext_dataset(df: pd.DataFrame, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"__label__{row['label']} {row['prompt']}\n")

    print(f"Saved {len(df)} rows to {output_path}")


def main(dataset_json_path: str, output_folder: str, test_size: float, seed: int) -> None:
    os.makedirs(output_folder, exist_ok=True)

    df = load_dataset(dataset_json_path)
    df = preprocess_dataset(df)

    train, test = split_dataset(df, test_size=test_size, seed=seed)

    save_fasttext_dataset(train, f"{output_folder}/train.fasttext")
    save_fasttext_dataset(test, f"{output_folder}/test.fasttext")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare and split dataset for FastText training")
    parser.add_argument(
        "--input", type=str, default="data/prompt-injections-dataset-labeled-full.json", help="Path to the input JSON dataset file"
    )
    parser.add_argument("--output", type=str, default="data/prompt-injections-split", help="Output folder for the split FastText datasets")
    parser.add_argument("--test-size", type=float, default=0.2, help="Proportion of the dataset to include in the test split")
    parser.add_argument("--seed", type=int, default=13, help="Random seed for reproducibility")

    args = parser.parse_args()

    main(args.input, args.output, args.test_size, args.seed)
