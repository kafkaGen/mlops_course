import argparse
import os
import shutil

import fasttext
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

import wandb

LABEL_MAPPING = {
    "Clean": 0,
    "Injection": 1,
}


def train_model(train_dataset_path: str, dim: int, epoch: int, lr: float, wordNgrams: int, loss: str) -> fasttext.FastText:

    print("\nModel training started.")

    model = fasttext.train_supervised(
        input=train_dataset_path,
        dim=dim,
        epoch=epoch,
        lr=lr,
        wordNgrams=wordNgrams,
        loss=loss,
    )

    print("Model training completed.")

    return model


def evaluate_model(model: fasttext.FastText, test_dataset_path: str, threshold: float = 0.5) -> dict:
    y_true = []
    y_pred = []

    with open(test_dataset_path, encoding="utf-8") as fl:
        for line in fl:
            parts = line.strip().split(" ", 1)
            label = parts[0].replace("__label__", "")
            text = parts[1]

            prediction = model.predict(text, k=2)
            prediction = dict(zip(tuple(map(lambda x: x.replace("__label__", ""), prediction[0])), prediction[1]))

            y_true.append(LABEL_MAPPING[label])
            y_pred.append(int(prediction["Injection"] > threshold))

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted")
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    cm = pd.DataFrame(cm, columns=list(LABEL_MAPPING.keys()), index=list(LABEL_MAPPING.keys()))

    print("\nModel evaluation results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "cm": cm.to_dict(),
    }


def log_model(wandb_run: wandb.sdk.wandb_run.Run, model: fasttext.FastText, metrics: dict, training_config: dict) -> None:
    os.makedirs("models", exist_ok=True)
    model_path = "models/fasttext_model.bin"
    model.save_model(model_path)

    artifact = wandb.Artifact(
        name="fasttext-prompt-injection-classifier",
        type="model",
        description=f"FastText model for prompt injection classification (F1: {metrics['f1']:.4f})",
    )

    artifact.add_file(model_path)
    artifact.metadata = {
        "metrics": metrics,
        "training_config": training_config,
    }

    wandb_run.log_artifact(artifact)

    shutil.rmtree("models", ignore_errors=True)


def main(
    train_dataset_path: str,
    test_dataset_path: str,
    dim: int,
    epoch: int,
    lr: float,
    wordNgrams: int,
    loss: str,
    threshold: float,
) -> None:
    training_config = {
        "dim": dim,
        "epoch": epoch,
        "lr": lr,
        "wordNgrams": wordNgrams,
        "loss": loss,
    }

    wandb_run = wandb.init(
        project="prompt-injection-classification",
        config={
            "training_config": training_config,
            "threshold": threshold,
        },
    )

    model = train_model(train_dataset_path, **training_config)
    metrics = evaluate_model(model, test_dataset_path, threshold=threshold)

    wandb_run.log(metrics)
    log_model(wandb_run, model, metrics, training_config)

    wandb_run.finish()


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Train FastText model for prompt injection classification")

    parser.add_argument("--train", type=str, default="data/prompt-injections-split/train.fasttext", help="Path to the training dataset")
    parser.add_argument("--test", type=str, default="data/prompt-injections-split/test.fasttext", help="Path to the test dataset")
    parser.add_argument("--dim", type=int, default=100, help="Size of word vectors")
    parser.add_argument("--epoch", type=int, default=25, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=0.1, help="Learning rate")
    parser.add_argument("--word-ngrams", type=int, default=2, help="Max length of word ngrams")
    parser.add_argument("--loss", type=str, default="softmax", choices=["ns", "hs", "softmax"], help="Loss function")
    parser.add_argument("--threshold", type=float, default=0.5, help="Classification threshold")

    args = parser.parse_args()

    main(
        train_dataset_path=args.train,
        test_dataset_path=args.test,
        dim=args.dim,
        epoch=args.epoch,
        lr=args.lr,
        wordNgrams=args.word_ngrams,
        loss=args.loss,
        threshold=args.threshold,
    )
