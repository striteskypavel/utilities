import anthropic

# Initialize client with your API key
client = anthropic.Anthropic(
    api_key="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"  # Replace with your actual API key
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="You are a world-class poet. Respond only with short poems.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the ocean salty?"
                }
            ]
        }
    ]
)
print(message.content)