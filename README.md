# chatgpt-talk
ChatGPTと会話するためのサンプル

# Usage
Windows以外では動作しません。
音声の読み上げにはSAPIを使用しているので以下の記事を参考に設定してください。

https://zenn.dev/reatoretch/articles/bb798223441d95


## インストール
```
pip install git+https://github.com/reatoretch/chatgpt-talk
```

## 環境変数
OpenAIのAPI_KEYを設定
![image](https://github.com/reatoretch/chatgpt-talk/assets/25296172/9c0e61c6-9a8f-4fdd-b97b-d1d1abc0e8ff)

```
OPENAI_API_KEY="YOUR_API_KEY"
```

## 使用例
sample.py
```python
from chatgpttalk import ChatGpt

TALK_LIMIT=10

def main():
    args = sys.argv
    if len(args)!=2:
        print("ex) python main.py JA|EN")
        exit()
    
    lang = args[1].lower()
    
    log_print = print
    gpt = ChatGpt(lang)
    for i in range(TALK_LIMIT):
        input(gpt.system_messages[0])
        gpt.record_voice()
        myvoice_text=gpt.voice_recognition()
        log_print(gpt.system_messages[1],myvoice_text)
        if not myvoice_text:exit("ERROR")
        gpt_response=gpt.conversation(myvoice_text)
        log_print(gpt_response)
        gpt.speak(gpt_response)

if __name__ == "__main__":
    main()
```
