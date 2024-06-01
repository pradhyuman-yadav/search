import _groq

response = _groq.chat_completion(messages=[
    _groq.user("My favorite color is blue."),
    _groq.assistant("That's great to hear!"),
    _groq.user("What is my favorite color?"),
])
print(response)
# "Sure, I can help you with that! Your favorite color is blue."