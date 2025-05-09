user_sentence = ""
last_word = ""

def get_input_dict():
    return {
        # "base_information": f"""Your task is to help an severely disabled user to communicate his needs. Therefore
        # you have to give back a list of 12 words that are most likely to contain the word the user wants
        # to include next in his sentence. The current sentence is: '{user_sentence}'. Only give back the words nothing else""",
        
        # "start": """Give me 12 common words that a sentence can start with.
        # Include nothing else in the response. Do not include numbers or any special characters.""",

        "general_information": f"""Your task is to help a severely disabled person to communicate only with his eyes. Therefore
        he will need a list with 12 words from which he can choose using an eyetracker. You have to provide the list of 12 words
        that fit in the context of the given, unfinished sentence. The focus of this program is on communication basic needs, so unnecessary words
        like 'please' or 'thanks' should never be considered. Only provide a list of 12 words separated by a space and nothing else,
        otherwise the program wont be able to handle it""",

        "nxt": f"""The current sentence is: '{user_sentence}'. Provide the next 12 words that will be shown to the user. Only provide a list of 12 words separated by a space and nothing else,
        otherwise the program wont be able to handle it"""
    }