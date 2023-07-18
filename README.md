MichurinAI_bot - VK bot with quiz and AI communication functionality

MichurinAI_bot is a VK bot created using the Python programming language and the vkbottle library. It provides several features to users, such as a quiz, AI communication, access to event posters, and the ability to suggest ideas.
Technical details:

The bot uses the vkbottle library to handle VK API requests and interact with users.
CtxStorage from vkbottle is used to store the quiz state and user responses.
Interaction with artificial intelligence is done through Google Dialogflow.
The bot retrieves its token and other settings from environment variables.
SQLite3 database is used to store information about events and landmarks.
How to use:

To interact with the bot, users can send commands in the VK chat. For example, the "Menu" command will display the list of available functions. To start the quiz, the user should enter "Quest" and follow the bot's instructions.
