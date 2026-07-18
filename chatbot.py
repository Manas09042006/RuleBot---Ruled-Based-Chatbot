import random
import re

from responses import responses


class ChatBot:

    def __init__(self):

        self.responses = responses


    def get_response(self, message):

        message = message.lower().strip()

        for pattern, response in self.responses.items():

            if re.search(pattern, message):

                if isinstance(response, list):
                    return random.choice(response)

                return response

        return "Sorry, I don't understand."