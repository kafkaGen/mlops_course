# Model Training and Evaluation (Phase 2)

This document outlines the second phase of the MLOps project, focusing on model development, training, evaluation, and registration. This phase implements a text classification solution for detecting prompt injections in user inputs.

## 1. Model Selection

**FastText** was selected as the classification model for the following reasons:

- Lightweight architecture that enables rapid training without GPU requirements
- Effective handling of text classification tasks with minimal preprocessing
- Support for word n-grams that can capture important patterns in injection attempts

## 2. Dataset Preparation

The labeled dataset from [Phase 1](./DataManagement.md) was processed using the `prepare_split_dataset.py` script, which performs the following operations:

- Loads the JSON-formatted labeled data
- Applies text preprocessing (lowercasing, whitespace normalization)
- Splits the dataset into training (80%) and testing (20%) sets with stratification
- Converts the data into FastText-compatible format

To prepare the dataset with custom parameters:

```bash
python src/train/prepare_split_dataset.py --input <path-to-json> --output <output-directory> --test-size 0.2 --seed 13
```

## 3. Model Training

The FastText model was trained using the `train.py` script, which supports customization of multiple hyperparameters:

```bash
python src/train/train.py --dim 100 --epoch 25 --lr 0.1 --word-ngrams 2 --loss softmax --threshold 0.5
```

Key hyperparameters include:

- `dim`: Size of word vectors (default: 100)
- `epoch`: Number of training iterations (default: 25)
- `lr`: Learning rate (default: 0.1)
- `word-ngrams`: Maximum length of word n-grams (default: 2)
- `loss`: Loss function (options: softmax, ns, hs)
- `threshold`: Classification threshold for binary decision (default: 0.5)

## 4. Model Evaluation

The trained model is evaluated on the test set with the following metrics:

- Accuracy: Overall correctness of predictions
- Precision: Ratio of true positive predictions to all positive predictions
- Recall: Ratio of true positive predictions to all actual positives
- F1 Score: Harmonic mean of precision and recall
- Confusion Matrix: Visualization of prediction performance across classes

## 5. Experiment Tracking and Monitoring

All training runs are tracked using Weights & Biases (W&B), providing:

- Comprehensive logging of hyperparameters
- Performance metrics visualization
- Confusion matrix visualization
- Model artifact storage
- Experiment comparison capabilities

To access the experiment results, log in to the W&B dashboard using the API key configured in the `.env` file.

## 6. Model Registry

Each trained model is automatically registered in the W&B Model Registry with:

- Model artifacts (binary files)
- Performance metrics
- Training configuration
- Dataset lineage information

This registry facilitates model versioning, selection of the optimal model for deployment, and reproducibility of results.

To select a model for deployment, compare experiment results in the W&B interface and promote the desired model version to production status.
