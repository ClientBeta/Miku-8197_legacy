# Miku-8197_legacy
Legacy Source of Miku Hatsune #8197

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
- google-generativeai
- os
- dotenv<br>

thats pretty much it since pip packages will automatically install it for you
while others are built in depedencies so u won't be bothered.

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
