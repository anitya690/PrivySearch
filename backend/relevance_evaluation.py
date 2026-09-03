import requests


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


top1_correct = 0
top3_correct = 0


print("PrivySearch Relevance Evaluation")
print("=" * 60)


for test in test_cases:

    query = test["query"]
    expected = test["expected"]

    response = requests.get(
        API_URL,
        params={"query": query}
    )

    response.raise_for_status()

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

    print(f"\nQuery: {query}")
    print(f"Expected: {expected}")
    print(f"Top Result: {top1}")
    print(f"Top-1: {'PASS' if top1_match else 'FAIL'}")
    print(f"Top-3: {'PASS' if top3_match else 'FAIL'}")


total = len(test_cases)

top1_accuracy = (top1_correct / total) * 100
top3_accuracy = (top3_correct / total) * 100


print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Top-1 Accuracy: {top1_accuracy:.2f}%")
print(f"Top-3 Accuracy: {top3_accuracy:.2f}%")