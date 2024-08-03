import tiktoken
enc = tiktoken.get_encoding("o200k_base")

# To get the tokeniser corresponding to a specific model in the OpenAI API:
#enc = tiktoken.encoding_for_model("gpt-4o")
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

with open("totokenize", "r") as txt:
    print(num_tokens_from_string(txt.read(), "o200k_base"))