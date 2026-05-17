from app.parsers.basic_parser import BasicParser

class  EventRouter:
    def __init__(self):
        self.log_parser = BasicParser()

    def process(self, event:dict)->dict:
        event_type = event.get("event_type")
        
        if event_type == "metric":
            return event
        return self.log_parser.parse(event)
        