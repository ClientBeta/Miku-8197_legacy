# Miku-8197_legacy
Legacy Source of Miku Hatsune #8197

## Dev Note :
F A A A A H

Recode of the main.py and changed memories.py to memory_manager.py for easier allocation

subside i added the one with fixed by ai since mine looks like a racoon just tried coding

## Info
this contains a legacy source of old chatbot miku hatunse which totally sucks because of the api sometimes not even answering.
most scripts here are either incomplete and have bugs and thats why i rewrote the entire scripture to a newer api provider
which is [openrouter](https://openrouter.ai).

## contents
- Structure
- Dependencies
- API
- Functions
- Tokens

## Structure
Main.py = Source of all which we know by now<br>
preference.txt = ai reads script and follows it<br>
storage.json = self explanation<br>
memories.py = how a dvd reads and write yk<br>
filter.json = filters what the ai and user says<br>
slash_commands.py = commands where you type / it shows commands<br>
ReactionLib.py = /reactions main source<br>
reactions.py = where the reactions examples are<br>

heres an illustration of where different files contribute to main.py<br>
```
                       ┌►.env                      
       ┌──────────────┐│   │                       
       │              ││ ┌─┘                       
preference.txt◄──────┐││ │                         
 │                   │││ │                         
 └►storage.json ◄───┐│││ │                         
         ▲ │  │     ││▼│ ▼                         
         │ │  └───► Main.py ◄─────────┬───────────┐
         │ ▼        ││▲ │             │           │
     memories.py◄───┘││ └─┬──►slash_commands.py   │
                     ▼│   └──►ReactioLib.py───────┘
                  filter.json      │   ▲           
                                   │   │           
                                   └─►reactions.py 
```

## Dependencies

- aiohappyeyeballs
- aiohttp
- aiosignal
- annotated-types
- attrs
- blinker
- cachetools
- certifi
- charset-normalizer
- click
- discord.py
- Flask
- frozenlist
- google-ai-generativelanguage
- google-api-core
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-generativeai
- googleapis-common-protos
- grpcio
- grpcio-status
- httplib2
- idna
- itsdangerous
- Jinja2
- MarkupSafe
- multidict
- propcache
- proto-plus
- protobuf
- pyasn1
- pyasn1_modules
- pydantic
- pydantic_core
- pyparsing
- python-dotenv
- requests
- rsa
- tqdm
- typing_extensions
- typing-inspection
- uritemplate
- urllib3
- Werkzeug
- yarl

some are not required lol

## API
this api uses gemini which is only good for tech support not for roleplaying
it uses 2.5-flash

which this line from main.py shows you the model and api call
```python
# Model Config
genai.configure(api_key=GoogleApi)
model=genai.GenerativeModel("gemini-2.5-flash")
```

heres the accurate doccumentation of google api/google-genai
[genai docs](https://github.com/googleapis/python-genai?tab=readme-ov-file)

## Functions
I js felt like adding this though i wont explain
but the main.py explains the code because the unrewritten one was ultra confusing
even the ai responded with "your alone on this one gng"

## Tokens
the .env stores all tokens to access the ai and discord bot
