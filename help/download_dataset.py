import json
import os

from datasets import load_dataset


def to_label_studio_format(ds, text_key="text", label_key="label", label_map=None, include_labels=True):
    ls_data = []
    for item in ds:
        entry = {"data": {"text": item[text_key]}}
        if include_labels:
            label_str = label_map[item[label_key]] if label_map else str(item[label_key])
            entry["annotations"] = [
                {
                    "result": [
                        {
                            "from_name": "label",
                            "to_name": "text",
                            "type": "choices",
                            "value": {
                                "choices": [label_str],
                            },
                        },
                    ]
                }
            ]
        ls_data.append(entry)
    return ls_data


def download_dataset(dataset_name, output_dir="./data"):
    os.makedirs(output_dir, exist_ok=True)

    label_map = {
        0: "Clean",
        1: "Injection",
    }

    dataset = load_dataset(dataset_name)

    train_formatted_data = to_label_studio_format(dataset["train"], label_map=label_map)
    test_formatted_data = to_label_studio_format(dataset["test"], label_map=label_map)

    with open(os.path.join(output_dir, f"{dataset_name.split('/')[-1]}_train.json"), "w", encoding="utf-8") as f:
        json.dump(train_formatted_data, f, ensure_ascii=False, indent=2)

    with open(os.path.join(output_dir, f"{dataset_name.split('/')[-1]}_test.json"), "w", encoding="utf-8") as f:
        json.dump(test_formatted_data, f, ensure_ascii=False, indent=2)


def main():
    download_dataset("deepset/prompt-injections", output_dir="./data")


if __name__ == "__main__":
    main()
