import requests
import time
import json
import os


API_URL = "http://127.0.0.1:8000/api/search"


test_cases = [
    {
        "query": "how to handle errors in Python",
        "expected": "8. Errors and Exceptions"
    },
    {
        "query": "how to create a Python class",
        "expected": "9. Classes"
    },
    {
        "query": "how to work with lists",
        "expected": "5. Data Structures"
    },
    {
        "query": "how to import modules",
        "expected": "6. Modules"
    },
    {
        "query": "how to read and write files",
        "expected": "7. Input and Output"
    },
    {
        "query": "how to use virtual environments",
        "expected": "12. Virtual Environments and Packages"
    },
    {
        "query": "how to use the Python interpreter",
        "expected": "2. Using the Python Interpreter"
    },
    {
        "query": "how to take input from a user",
        "expected": "7. Input and Output"
    },
    {
        "query": "what are exceptions in Python",
        "expected": "8. Errors and Exceptions"
    },
    {
        "query": "how to control program flow",
        "expected": "4. More Control Flow Tools"
    }
]


# -----------------------------
# Warm-up
# -----------------------------

print("Warming up search service...")

requests.get(
    API_URL,
    params={"query": "python"}
)

print("Warm-up complete.")


# -----------------------------
# Evaluation
# -----------------------------

top1_correct = 0
top3_correct = 0
latencies = []

results_report = []


for test in test_cases:

    query = test["query"]
    expected = test["expected"]

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

    titles = [
        result["title"]
        for result in results
    ]

    top1 = titles[0] if titles else "No result"

    top1_match = top1 == expected
    top3_match = expected in titles[:3]

    if top1_match:
        top1_correct += 1

    if top3_match:
        top3_correct += 1


    results_report.append({
        "query": query,
        "expected": expected,
        "top_result": top1,
        "top1": top1_match,
        "top3": top3_match,
        "latency_ms": round(latency, 2)
    })


# -----------------------------
# Metrics
# -----------------------------

total = len(test_cases)

top1_accuracy = (
    top1_correct / total
) * 100

top3_accuracy = (
    top3_correct / total
) * 100


sorted_latencies = sorted(latencies)

average_latency = (
    sum(latencies) / len(latencies)
)

p50 = sorted_latencies[
    len(sorted_latencies) // 2
]

p95_index = int(
    len(sorted_latencies) * 0.95
) - 1

p95 = sorted_latencies[
    max(0, p95_index)
]


# -----------------------------
# Report
# -----------------------------

report = {
    "total_queries": total,
    "top1_accuracy": round(top1_accuracy, 2),
    "top3_accuracy": round(top3_accuracy, 2),
    "average_latency_ms": round(average_latency, 2),
    "p50_latency_ms": round(p50, 2),
    "p95_latency_ms": round(p95, 2),
    "results": results_report
}


# Create output directory
os.makedirs("evaluation", exist_ok=True)


# Save JSON
with open(
    "evaluation/evaluation_report.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=2,
        ensure_ascii=False
    )


# -----------------------------
# Console Output
# -----------------------------

print("\n" + "=" * 60)
print("PRIVYSEARCH EVALUATION REPORT")
print("=" * 60)

print(f"Total Queries: {total}")
print(f"Top-1 Accuracy: {top1_accuracy:.2f}%")
print(f"Top-3 Accuracy: {top3_accuracy:.2f}%")
print(f"Average Latency: {average_latency:.2f} ms")
print(f"P50 Latency: {p50:.2f} ms")
print(f"P95 Latency: {p95:.2f} ms")

print("\nReport saved to:")
print("evaluation/evaluation_report.json")