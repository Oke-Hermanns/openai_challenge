import input_data
import requests

api_key = "Insert api key here"


url = "https://api.openai.com/v1/responses"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "temperature": '0.2'
}

data = {
    "model": "gpt-4.1"
}

def choose_word(words):
    print(words)
    number = int(input("enter the position of the word.\n"))
    input_data.user_sentence = input_data.user_sentence + " " + words[number]
    input_data.last_word = words[number]
    print(input_data.user_sentence)


def choose_promt(input_dict, last_word):
    if input_data.last_word == "":
        data["input"] = input_dict["base_information"]
    elif input_data.last_word == "end":
        return True
    else:
        data["input"] = input_dict["base_information"] # use other promt here, when history is stored

def make_promt():
    input_dict = input_data.get_input_dict()
    last_word = input_data.last_word
    response = choose_promt(input_dict, last_word)
    if response:
        return True

    re = requests.post(url, headers=headers, json=data)
    response_json = re.json()
    output_text = response_json["output"][0]["content"][0]["text"]
    words = output_text.split()
    choose_word(words)


def main():
    for i in range(0,12): # more than 12 words should not be necessary
        make_promt()

if __name__=="__main__":
    main()