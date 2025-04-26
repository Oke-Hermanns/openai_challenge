from openai import OpenAI
import input_data
client = OpenAI()

messages = [{"role": "system", "content": input_data.get_input_dict()["general_information"]}]

def create_response(input_text, temperature=0.2, model="gpt-4.1"):
    messages.append({"role": "user", "content": input_text})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    chatgpt_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chatgpt_reply})

    return chatgpt_reply

def choose_promt(input_dict, last_word):
    return input_dict["nxt"]

def make_promt():
    input_dict = input_data.get_input_dict()
    last_word = input_data.last_word
    response = choose_promt(input_dict, last_word)
    words = []
    while(len(words)!= 12):
        answer = create_response(response)
        words = answer.split()
    return words