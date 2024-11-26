import asyncio
import time
from ably import AblyRealtime
from translate import Translator


async def main():

  # Connect to Ably with your API key
  ably = AblyRealtime('*****************************')  # replace with API Key
  await ably.connection.once_async('connected')
  print('Connected to Ably')

  # Create a channel called 'get-started' and register a listener to subscribe to all messages with the name 'first'
  channel = ably.channels.get('get-started')

  # Define a listener function that takes a language prefix
  def create_listener(language_prefix):
      translator = Translator(to_lang=language_prefix)
      def listener(message):
          # print(f'{language_prefix} Message received: {message.data}')
          translation = translator.translate(message.data)
          print(f'{language_prefix} - Message Received: {translation}')

      return listener

  # Create and subscribe listeners for each language
  languages = ['de', 'fr', 'es', 'it', 'da', 'zh-tw']
  for lang in languages:
      await channel.subscribe('first', create_listener(lang))

  # Publish a message
  time.sleep(1)
  print('-----')
  msg = 'I made a joke about an API yesterday. Sadly, it didn’t get a response.'
  print('Publishing Message:', msg, '\n-----')
  await channel.publish('first', msg)


  # Close the connection to Ably after a 5 second delay
  time.sleep(2)
  await ably.close()
  print('-----')
  print('Closed the connection to Ably')

asyncio.run(main())
