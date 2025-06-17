import argparse
import asyncio
import json
import random
import time
from pathlib import Path
from urllib.parse import urlencode

import aiohttp


async def send_request(session: aiohttp.ClientSession, url: str, prompt: str):
    try:
        params = {"prompt": prompt}
        full_url = f"{url}?{urlencode(params)}"
        async with session.get(full_url) as response:
            if response.status != 200:
                print(f"Error {response.status} for prompt: {prompt[:30]}...")
            return await response.text()
    except Exception as e:
        print(f"Request failed: {e}")


async def stress_test(
    dataset: list[dict],
    url: str,
    duration: int,
    min_batch: int,
    max_batch: int,
    min_delay: float,
    max_delay: float,
):
    print("Starting stress test...")

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < duration:
            batch_size = random.randint(min_batch, max_batch)
            delay = random.uniform(min_delay, max_delay)
            batch = random.sample(dataset, batch_size)

            tasks = [send_request(session, url, sample["data"]["text"]) for sample in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(delay)

    print("Stress test completed.")


def main(args: argparse.Namespace):
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    with open(dataset_path) as f:
        dataset = json.load(f)

    asyncio.run(
        stress_test(
            dataset,
            url=args.url,
            duration=args.duration,
            min_batch=args.min_batch,
            max_batch=args.max_batch,
            min_delay=args.min_delay,
            max_delay=args.max_delay,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async Stress Test for Model API")
    parser.add_argument("--dataset", type=str, required=True, help="Path to the dataset JSON file")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000/model/inference",
        help="API endpoint URL",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=300,
        help="Stress test duration in seconds (default: 300s = 5min)",
    )
    parser.add_argument("--min-batch", type=int, default=30, help="Minimum sample size")
    parser.add_argument("--max-batch", type=int, default=100, help="Maximum sample size")
    parser.add_argument("--min-delay", type=float, default=0.1, help="Minimum delay between batches (s)")
    parser.add_argument("--max-delay", type=float, default=3.0, help="Maximum delay between batches (s)")

    args = parser.parse_args()

    main(args)
