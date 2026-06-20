import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.agent import run_agent

questions = ["个地区的销售总额多少？"]

for question in questions:
    print(f"\n问题: {question}")
    print("-" * 40)

    result = run_agent(question)

    print("Agent steps:")
    for step in result["steps"]:
        print(f" -> {step['tool']}({step['input']})")
    
    print(f"\nFinal answer: \n {result['answer']}")