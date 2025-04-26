user_sentence = ""
last_word = ""

def get_input_dict():
    return {
        "base_information": f"""Your task is to help an severely disabled user to communicate his needs. Therefore
        you have to give back a list of 13 words that are most likely to contain the word the user wants
        to include next in his sentence. The current sentence is: '{user_sentence}'. Only give back the words nothing else""",
        
        "start": """Give me 13 common words that a sentence can start with.
        Include nothing else in the response. Do not include numbers or any special characters.""",
    }