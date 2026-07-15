text = "the cat sat on the mat. the dog ran in the park."
words = text.split()

# Self-supervised: the "label" comes from the text itself, no human needed
training_pairs = [(words[:i], words[i]) for i in range(1, len(words))]

print(
    f"Generated {len(training_pairs)} training pairs from {len(words)} words")
for context, target in training_pairs[:5]:
    print(context, "->", target)
