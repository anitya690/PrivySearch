import time
import requests


queries = [
    "how to handle errors in Python",
    "how to create a Python class",
    "how to work with lists",
    "how to import modules",
    "how to read and write files",
    "how to use virtual environments",
    "how to take input from a user",
    "how to use the Python interpreter",
    "what are exceptions in Python",
    "how to control program flow"
]


API_URL = "http://127.0.0.1:8000/api/search"


print("PrivySearch Evaluation")
print("=" * 50)


# -----------------------------
# Warm-up Request
# -----------------------------
# This removes model-loading/cold-start
# overhead from the actual benchmark.

print("\nWarming up search service...")

requests.get(
    API_URL,
    params={"query": "python"}
)

print("Warm-up complete.")


# -----------------------------
# Benchmark
# -----------------------------

latencies = []


for query in queries:

    start = time.perf_counter()

    response = requests.get(
        API_URL,
        params={"query": query}
    )

    end = time.perf_counter()

    response.raise_for_status()

    latency = (end - start) * 1000

    latencies.append(latency)

    data = response.json()

    results = data.get("results", [])

    print(f"\nQuery: {query}")

    if results:

        print(
            f"Top Result: {results[0]['title']}"
        )

        print(
            f"Hybrid Score: "
            f"{results[0].get('hybrid_score', 0):.2f}"
        )

    print(
        f"Latency: {latency:.2f} ms"
    )


# -----------------------------
# Statistics
# -----------------------------

print("\n" + "=" * 50)

average_latency = (
    sum(latencies) / len(latencies)
)

sorted_latencies = sorted(latencies)

p50_index = len(sorted_latencies) // 2
p50 = sorted_latencies[p50_index]

p95_index = int(
    len(sorted_latencies) * 0.95
) - 1

p95 = sorted_latencies[
    max(0, p95_index)
]


print(
    f"Average Latency: "
    f"{average_latency:.2f} ms"
)

print(
    f"P50 Latency: "
    f"{p50:.2f} ms"
)

print(
    f"P95 Latency: "
    f"{p95:.2f} ms"
)