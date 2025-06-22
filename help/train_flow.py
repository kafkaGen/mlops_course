import argparse
import os
import subprocess

import yaml


def run_command(command: str):
    print(f"Running command:\n{command}\n")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {command}")


def main(config: dict = None) -> None:
    # Download the latest dataset
    print("Downloading the latest dataset...\n\n")
    run_command("dvc pull ./data/prompt-injections-dataset-labeled-full.json.dvc")

    # Prepare and split the dataset
    print("\n\nPreparing and splitting the dataset...\n\n")
    prepare_dataset_args = " ".join([f"--{arg_name} {arg_value}" for arg_name, arg_value in config["dataset_prepare_config"].items()])
    run_command(f"python src/train/prepare_split_dataset.py {prepare_dataset_args}")

    # Train the FastText model
    print("\n\nTraining the FastText model...\n\n")
    train_args = " ".join([f"--{arg_name} {arg_value}" for arg_name, arg_value in config["train_config"].items()])
    run_command(f"python src/train/train.py {train_args}")

    # Clean up
    print("\n\nCleaning up...\n\n")
    run_command(f'rm -r {config["dataset_prepare_config"]["output"]}')
    if os.path.exists("./wandb"):
        run_command("rm -r ./wandb ")

    print("Training completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare data and train FastText model for prompt injection classification")
    parser.add_argument("--config-path", type=str, default="configs/training/train.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    with open(args.config_path) as file:
        config = yaml.safe_load(file)

    main(config)
