# AutomatizaCF

## Introduction

A manager and chatbot event-oriented to Colégio Fantástico.

Receives messages from the meta API and responds with the conversation flow determined in messages_tree.json and upon arriving at the end of the conversation flow (tree) forwards the messages to the service sector where you can respond without having to enter whatsapp propiamente said. 

In addition, some more functions such as registering input and output of students, virtual calendar and others. 

As far as chat bot is concerned there is also a class for commands (including openAI API support)

## How to execute
```cmd
python3 main.py
```
