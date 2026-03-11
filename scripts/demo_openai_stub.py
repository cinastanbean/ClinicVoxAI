from __future__ import annotations

from app.llm.openai_client import OpenAIIntentClassifier, OpenAIReportSummarizer


def run() -> None:
    classifier = OpenAIIntentClassifier()
    summarizer = OpenAIReportSummarizer()

    print(classifier.classify("I want to schedule an appointment"))
    print(summarizer.summarize("Impression: Mild degenerative changes in L4-L5."))


if __name__ == "__main__":
    run()
