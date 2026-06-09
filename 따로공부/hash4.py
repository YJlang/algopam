from collections import Counter

participant = ["leo", "kiki", "eden"]
completion = ["eden", "kiki"]

result = Counter(participant) - Counter(completion)

print(list(result.items())[0][0])