import ijson
import json


def initialize_parser(file):
    '''
    Given a file object, this returns an ijson parser (which is a python iterator)
    '''
    file.seek(0)
    return ijson.basic_parse(f)


def print_all_events(parser):
    '''
    An example of how to iterate through events using the parser.  The events consist of tuples:

        (event_type, content)

    If the parser is setup on the example data, the loop below will print out these events:

    (u'start_map', None)
    (u'map_key', u'earth')
    (u'start_map', None)
    (u'map_key', u'europe')
    (u'start_array', None)
    (u'start_map', None)
    (u'map_key', u'name') ... etc ...

    '''
    for e in parser:
        print(e)

'''
def build_from_events(parser):

    A json object can be re-built from events using the ObjectBuilder.

    This is useful if you want to capture a subset of the events and reconstruct some json

    Below we loop through all parsed events and reconstruct the original json

    ob = ijson.ObjectBuilder()  # initialize an ObjectBuilder
    for e in parser:
        ob.event(e[0], e[1])    # give the object builder the first and second part of the event tuple
    return ob.value             # the value property of the ObjectBuilder contains the json built up from events
'''
def build_from_events(parser):
    '''
    A json object can be re-built from events using the ObjectBuilder.

    This is useful if you want to capture a subset of the events and reconstruct some json

    Below we loop through all parsed events and reconstruct the original json
    '''
    ob = ijson.ObjectBuilder()  # initialize an ObjectBuilder
    for e in parser:      
        ob.event(e[0], e[1])    # give the object builder the first and second part of the event tuple
    return ob.value             # the value property of the ObjectBuilder contains the json built up from events

def max_nesting(parser):
    '''
    ------- WRITE THIS FUNCTION FIRST ------------

    Return the maximum nesting of json objects in the parsed events.
    
    Arrays don't count as a level of nesting.
    
    On the example data, this should return 4. 

     
    '''
    max_nest = 0
    
    current_nest_number = 0
    
    for e in parser:
        if e[0] == "start_map":
            current_nest_number = current_nest_number + 1
            if current_nest_number > max_nest:
                max_nest = current_nest_number
        if e[0] == "end_map":
            current_nest_number = current_nest_number - 1
            
    return max_nest


def extract_by_key(parser, key_value):
    '''
    ------- THEN WRITE THIS FUNCTION ------------

    Return a list of values (string, object, or array) that is associated with a key equal to 'key_value'
    (You can ignore nested occurrences of 'key-value', returning only the outer-most one)

    for example, if key-value is 'info' it should return:

    [
        { "1":"1" },
        { "2":"2" },
        { "2":"2" }
    ]

    if key-value is 'america' it should return:

    [
        [ {"name": "Texas", "type": "state", "info": { "2":"2" }} ]
    ]

    if key-value is '2' it should return:
    [
        "2",
        "2"
    ]

    Hint: Start by understanding the output of print_all_events().
    Make use of the methods provided and gain insights from writing the 
    max_nesting() method. 

    '''
    ret = []
    
    json_string = str(build_from_events(parser))
    json_string = json_string.replace("'","\"")
    parsed_json = json.loads(json_string)
    #print(parsed_json.get('earth').get('america')[0].get("info").get('2'))
    
    #for level in range(max_nesting(parser)):
    for key1 in (parsed_json.keys()):
        if (key1 == key_value):
            ret.append(parsed_json.get(key1))
        for key2 in (parsed_json.get(key1)):
            if (key2 == key_value):
                ret.append(parsed_json.get(key1).get(key2))
            for i in range(len(parsed_json.get(key1).get(key2))):      
                for key3 in (parsed_json.get(key1).get(key2)[i]):
                    if (key3 == key_value):
                        ret.append(parsed_json.get(key1).get(key2)[i].get(key3))
                    for key4 in (parsed_json.get(key1).get(key2)[i].get(key3)):
                        if (key4 == key_value):
                            ret.append(parsed_json.get(key1).get(key2)[i].get(key3).get(key4))

    # populate the list ret

    return ret



                
if __name__ == '__main__':

    filename = 'test.json'
    with open(filename, 'r') as f:
        parser = initialize_parser(f)
        print(max_nesting(parser))
        parser = initialize_parser(f)
        print(extract_by_key(parser, 'info'))
        






