import enum

class JsonStates(enum.Enum):
    BracketOpen = 1 #[
    BracesOpen = 2  #{
    PromptKey = 3   #"prompt": 
    PromptString = 4
    Comma = 5
    Name = 6        #"name": "
    #get logits from model to predict function name
    CloseQuotes = 7 #"
    Prameters = 8   #"parameters": {<get these from the functions file you already have the name>}
    CloseParanthesis = 9 #}
    Next = 10       #,
