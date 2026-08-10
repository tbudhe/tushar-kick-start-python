from rag_service import answer_question

TEST_CASES = [
    {"question": "How do I add a door in Revit?", "expected_id": "doc3"},
    {"question": "How do I add a floor in Revit?", "expected_id": "doc5"},
    {"question": "How do I add a window in Revit?", "expected_id": "doc2"},
    {"question": "What's the capital of France?",
        "expected_answer": "I don't know"},
    {"question": "How do I create a wall in Revit?", "expected_id": "doc4"},
]


def run_case(case):
    # Same function the API uses — evals test the real pipeline
    resp = answer_question(case["question"])
    answer, sources = resp.answer, [s.id for s in resp.sources]

    if "expected_answer" in case:
        passed = answer.strip() == case["expected_answer"]
    else:
        passed = case["expected_id"] in sources

    detail = f"sources={sources} answer={answer!r}"

    return passed, detail


def main():
    results = []
    for case in TEST_CASES:
        passed, detail = run_case(case)
        results.append(passed)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {case['question']} -- {detail}")

    total = len(results)
    passed_count = sum(results)
    print(f"\n{passed_count}/{total} passed")


if __name__ == "__main__":
    main()
