# def hash_of_string(s):
#     return sum(ord(c) for c in s)
#
# text = input().strip()
#
# words = text.split()
#
# words.sort(key=lambda x: (hash_of_string(x) if x != "ADAUniversity" else -1, x))
#
# for word in words:
#     print(word)

# INPUT HANDLING

def hash_of_string(s):
    return sum(ord(c) for c in s)

file_path = 'input (3).txt'

with open(file_path, 'r') as file:
    words = file.read().split()

words.sort(key=lambda x: (hash_of_string(x) if x != "ADAUniversity" else -1, x))

hash_s306 = hash_of_string(words[305])

print(hash_s306)
