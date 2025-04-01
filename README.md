## Using Language Models for Narrative and Contextual Dialogue
Language models, on the other hand, excel in areas like narrative generation, dialogue systems, and understanding textual context. In an MMORPG, language models could be used for:
* In-game NPC dialogue: Providing dynamic, context-sensitive conversations that enhance the story and player immersion.
* Player behavior analysis: Analyzing player speech or written content (e.g., chat logs) to infer their intentions, mood, or strategy, which could influence how NPCs or the AI boss react.
* Event or quest generation:
Hybrid Approach: Combining RL and LM
A hybrid system could involve the following:
1. Contextual Awareness:
    * The language model can analyze the environmental context, player actions, or game world state (e.g., analyzing a quest or combat narrative) and pass that data to the RL model.
    * The RL model then makes tactical decisions based on this input (e.g., whether to attack, retreat, or use a specific skill).
2. RL for Action, LM for Strategy Enhancement:
    * The RL model could focus on action selection (combat, movement, etc.), while the language model can generate high-level strategies or insights, offering suggestions for long-term goals or adjusting the AI's tactics dynamically based on player strategies and evolving game conditions.
    
    
    ### 환경설정

가상 환경 만들고 .env 파일 만들어서 UPSTAGE API Key 넣어주세요. 예시 .env 파일은 .env.example에서 찾을 수 있습니다.

```
python -m venv venv
source venv/bin/activate
pip install --upgrade --quiet  langchain langchain-community python-dotenv langchain-core langchain-upstage
python chatbot.py
```

학습시킬 예시 PDF 파일에 들어갈 텍스트는 test.txt 파일에서 찾을 수 있습니다.
