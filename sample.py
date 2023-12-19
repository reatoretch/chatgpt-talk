from chatgpt_talk import ChatGpt

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