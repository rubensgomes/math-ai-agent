review openai functions:
https://developers.openai.com/api/docs/guides/function-calling

review rubens chatgpt chat:
https://chatgpt.com/g/g-p-68d201df829881918fd59a03bfcbf2e8-ai-development/c/69ad64c5-c650-8332-8fd6-43a94af8a80f


OpenAI API Python SDK
- You can enable logging by setting the environment variable OPENAI_LOG to info.

  $ export OPENAI_LOG=info

# Configure the default for all requests:
client = OpenAI(
    # 20 seconds (default is 10 minutes)
    timeout=20.0,
)

# More granular control:
client = OpenAI(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)


## src/math_ai_agent/app.py
- break the app.py code into modular areas, and delegate calls to modules.  
  Need to see patterns used in OpenAI codebase
- check if the tool requested by the LLM is supported or registered
- add number of tokens consumed in error log when LLM reaches limit
- create a debug log message that displays several details in the LMM 
  response including number of tokens consumed so far
- add exceptions types (e.g., security exception when llm does not accpe 
  content)
- should we use some AI Python framework for coding agents?