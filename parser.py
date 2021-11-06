import json
import itertools
from operator import itemgetter
from bs4 import BeautifulSoup

DataTypes = {
    str: "string",
    float: "float",
    int: "integer",
    # double: "double",
}

class InvalidHtmlException(Exception):
    pass

class HTMLParser(object):
    
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
    
    @property
    def parsed_data(self):
        rows = self.soup.find_all(
            "div", {"class": lambda value: value and value.startswith("user-") }
        )
        parsed_data = []
        for row in rows:
            time_stamp  = row.find("t").text.replace('[','').replace(']','')
            users, message = row.find("span").text.split(": ")
            users = [ user.replace('[','').replace(']','').strip() for user in users.replace("♦️", "").replace("♥", "").split("► ") ]
            # print(f"time_stamp:{time_stamp} users: {users} chat:{chat}\n")
            parsed_data.append(
                dict(
                    time_stamp=time_stamp,
                    users=users,
                    message=message
                    
                )
            )
        return sorted(parsed_data, key=itemgetter('time_stamp')) 
    
    
    @property
    def chat_users(self):
        users = set()
        for d in self.parsed_data:
            users.update(d['users'])
        if not users:
            raise InvalidHtmlException("Invalid Html File!")
        return sorted(list(users))
    
    
    def chat_user_index(self, chat_user):
        return self.chat_users.index(chat_user)+1
    
    
    def message_time_stamp(self, chat_user, first=True):
        """return first message timestamp if first -> true else last message timestamp"""
        return [ 
            d for d in self.parsed_data if chat_user in d["users"][0]
        ][0 if first else -1]['time_stamp']
    
    
    @property
    def chat_data(self):
        return [
            dict(
                USERNAME=chat_user,
                FIRST_MESSAGE_TIMESTAMP=self.message_time_stamp(chat_user, first=True),
                LAST_MESSAGE_TIMESTAMP=self.message_time_stamp(chat_user, first=False)
            )
            for chat_user in self.chat_users
        ]
    
    def users_conversation(self, user1, user2):
        return [ 
            d for d in self.parsed_data 
            if len(d["users"]) > 1 and user1 in d["users"][0] 
            and user2 in d["users"][1]
        ]
    
    @property
    def conversation_data(self):
        conversation_data = []
        for user1, user2 in itertools.combinations(self.chat_users, 2):
            user1_with_user2 = self.users_conversation(user1, user2)
            user2_with_user1 = self.users_conversation(user2, user1)
            # conversation_count = round(float(user1_with_user2 + user2_with_user1), 2)
            # conversation_data.append(
            #     dict(
            #         source=user1,
            #         target=user2,
            #         weight= conversation_count,
            #     )
            # )
            conversation_data.append(
                dict(
                    source=user1,
                    target=user2,
                    weight= round(float(len(user1_with_user2)),2),
                )
            )
            conversation_data.append(
                dict(
                    source=user2,
                    target=user1,
                    weight= round(float(len(user2_with_user1)),2),
                )
            )            
        return sorted(conversation_data, key=itemgetter('source'))
    
    
    @property    
    def graph_data(self):
        chat_data = self.chat_data
        data = dict(
            key = [
                {
                    "@id": key,
                    "@for": "node",
                    "@attr.name": key.lower(),
                    "@attr.type": DataTypes.get(type(value))
                } for key, value in chat_data[0].items()
            ],
            graph = dict(
                node = [
                    {
                       "@id": self.chat_user_index(chat["USERNAME"]),
                       "data": [
                           {
                                "@key": key,
                                "#text": value
                            } for key, value in chat.items()
                       ]
                    } for chat in chat_data
                ]
            ),
            edge = [
                {
				"@source": self.chat_user_index(convo["source"]),
				"@target": self.chat_user_index(convo["target"]),
				"@weight": convo["weight"]
			    } for convo in self.conversation_data
            ]
        )
        return data


if __name__ == '__main__':
    with open('./html/chat.html', 'r') as f:
        html_string = f.read()
        try:
            parser = HTMLParser(html=html_string)
            print(json.dumps(parser.graph_data, indent=2))
        except InvalidHtmlException as e:
            print("InvalidHtmlException > {e}")
    
    # with open('./html/chat-wrapped.html', 'r') as f:
    #     html_string = f.read()
    #     parser = HTMLParser(html=html_string)
    #     print(json.dumps(parser.graph_data, indent=2))

