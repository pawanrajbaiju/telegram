# Importing Modules
import requests
import pandas as pd

# Questions Files Link
url = "https://raw.githubusercontent.com/pawanrajbaiju/telegram/main/qna_chitchat_professional.tsv"
input = "/content/drive/MyDrive/Colab Notebooks/Question.csv"
df = pd.read_csv(url, sep="\t")

# Base url for getting user message...
base_url = "https://api.telegram.org/bot5574969249:AAHbBAF82Fz6YzJ0LU4s6oeXpKPXdFqz2SA"


# Read Message which is sent by user
def read_msg(offset):
  parameters = {
      "offset" : offset,
  }
  resp = requests.get(base_url + "/getUpdates", data=parameters)
  data = resp.json()
  print(data)
  
  for result in data['result']:
    if 'text' in result['message']:
      send_msg(result)

  if data['result']:
    return data['result'][-1]['update_id'] + 1


# Auto Reply through the file which is written by the author.
def auto_answer(message):
  answer = df.loc[df['Question'].str.lower() == message.lower()]
  
  if not answer.empty:
    answer = answer.iloc[0]['Answer']
    return answer
  else:
    print(message)
    with open(input, 'a') as f:
      f.write(str(message + "\n"))
      f.close()
    return "Sorry, I could not understand You !!! : I am still learning and try to better in answering."
    

# Sending message to the user 
def send_msg(message):
  text = message['message']['text']
  message_id = message['message']['message_id']
  answer = auto_answer(text)
  chat_id = message['message']['chat']['id']
 
  parameters = {
      "chat_id" : chat_id,
      "text" : answer,
      "reply_to_message_id" : message_id
  }

  resp = requests.get(base_url + "/sendMessage", data=parameters)
  print(resp.text)

offset = 0
while True:
  offset = read_msg(offset)