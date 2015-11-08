# Create the category with some positive (and negative) examples, and a name.
pos = [
    "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.",
    "To iterate is human, to recurse divine.",
    "First learn computer science and all the theory. Next develop a programming style. Then forget all that and just hack."
    ]
neg = [
    "To err is human, to forgive divine."
    ]
categoryName = "programming quotes"
programmingCategory = client.createClassification(categoryName, pos, neg)

# Evaluate how close a new term is to the category.
termBitmap = client.getBitmap("Python")['fingerprint']['positions']
distances = client.compare(termBitmap, programmingCategory['positions'])
print distances['euclideanDistance']

# Try a block of text.
textBitmap = client.getTextBitmap("The Zen of Python >>>import this")['fingerprint']['positions']
distances = client.compare(textBitmap, programmingCategory['positions'])
print distances['euclideanDistance']
