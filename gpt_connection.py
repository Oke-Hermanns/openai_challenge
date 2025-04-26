from openai import OpenAI
import input_data
client = OpenAI()

def create_response(input_text, temperature=0.2, model="gpt-4.1"):
    response = client.responses.create(
        model=model,
        input=input_text,
        temperature=temperature
    )
    return response.output_text

def choose_word(words):
    print(words)
    number = int(input("enter the position of the word.\n"))
    input_data.user_sentence = input_data.user_sentence + " " + words[number]
    input_data.last_word = words[number]
    print(input_data.user_sentence)


def choose_promt(input_dict, last_word):
    if last_word == "":
        return input_dict["base_information"]
    elif last_word == "end":
        return None
    else:
        return input_dict["base_information"] # use other promt here, when history is stored

def make_promt():
    input_dict = input_data.get_input_dict()
    last_word = input_data.last_word
    response = choose_promt(input_dict, last_word)
    if response is None:
        return True

    answer = create_response(response)
    words = answer.split()
    choose_word(words)


def main():
    for i in range(0,12): # more than 12 words should not be necessary
        make_promt()

if __name__=="__main__":
    main()