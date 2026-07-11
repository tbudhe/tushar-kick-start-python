import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

text = " Hope the day is beautiful"

token_ids = enc.encode(text)

tokens = [enc.decode([id]) for id in token_ids]

print("Token IDs:", token_ids)
print("Token: ", tokens)
