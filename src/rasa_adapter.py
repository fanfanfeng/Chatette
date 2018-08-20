#!/usr/bin/env python3

from utils import *


def to_Rasa_format(intent_name, example, entities):
    rasa_entities = []
    for entity in entities:
        first_index = example.find(entity["text"])
        if first_index == -1:
            import warnings
            warnings.warn("Couldn't find '"+entity["text"]+"' inside '"+
                example+"'. This is a bug in the generator, the example "+
                "will be discarded.")
            return None
        else:
            rasa_entities.append({
                "value": entity["value"],
                "entity": entity["slot-name"],
                "start": first_index,
                "end": first_index+len(entity["text"]),
            })

    return {
        "text": example,
        "intent": intent_name,
        "entities": rasa_entities,
    }


{
        "entities": [
          {
            "end": 8,
            "entity": "utilization",
            "start": -1,
            "value": "60"
          }
        ],
        "intent": "inform_utilization",
        "text": "only 60%"
      },
