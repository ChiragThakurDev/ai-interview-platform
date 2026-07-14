from app.ai.llm import get_llm

llm=get_llm()

response=llm.invoke("say hello.")

print(response.content)
