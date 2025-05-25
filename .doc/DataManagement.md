# Data Management (Step 1)

The first phase of the project focuses on setting up a robust data management pipeline, including:

## 1. Start Required Services

To start or restart all required services (Label Studio, MinIO, etc.), run:

```bash
make start-services
```

## 2. Data Acquisition

The project uses the `deepset/prompt-injections` dataset from Hugging Face, which contains examples of clean and malicious prompts. The dataset is downloaded using the helper script:

```bash
python help/download_dataset.py
```

This script:

- Downloads the dataset from Hugging Face
- Converts it to a format compatible with Label Studio
- Saves train and test splits in the `data/` directory

## 3. MinIO Setup

After starting the MinIO service, the following manual steps were performed:

1. Access the MinIO Console at http://localhost:9001 and log in using credentials from the `.env` file
2. Create three dedicated buckets:
   - `prompt-injections-raw-data` - for storing raw text data (prompts)
   - `prompt-injections-labeled-data` - for storing labeled data exported from Label Studio
   - `prompt-injections-dataset-dvc-storage` - for DVC remote storage

## 4. Data Labeling with Label Studio

The project uses Label Studio for data annotation and management. The following manual steps were performed:

1. Access Label Studio at http://localhost:8080 and create a user account
2. Create a new project for text classification and configure the labeling interface
3. Set up synchronization between Label Studio and MinIO for data storage
4. Manually upload initial data samples for labeling
5. Import pre-labeled data from the Hugging Face dataset
6. Perform labeling using the binary classification schema (Clean/Injection)
7. Export the complete labeled dataset in JSON format

## 5. Data Versioning with DVC and MinIO

The project uses DVC with MinIO as remote storage for dataset versioning:

1. Initialize DVC:

   ```bash
   dvc init
   ```

2. Configure MinIO as remote storage:

   ```bash
   dvc remote add -d minio s3://prompt-injections-dataset-dvc-storage/
   dvc remote modify minio endpointurl http://localhost:9000
   ```

3. Add the dataset to DVC:

   ```bash
   dvc add data/prompt-injections-dataset-labeled-full.json
   ```

4. Commit and push changes:

   ```bash
   git add .
   git commit -m "Add labeled dataset"
   dvc push
   ```
