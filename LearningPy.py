import sys
import json
import jsonschema


schema = {
  "type": "object",
  "properties": {
    "payload":      {
        "type": "object",
        "properties": {
            "user": {
                "type": "string"
            } ,
            "filter": {
                "type": "string"
            }
        },
        "required": ["user", "filter"]
        }
    },
  "required": ["payload"]
}


def loadJson():
    jsoncontent =  "{'operation': 'create', 'payload': { 'user': 'unitLambda', 'filterz': 'xyz'}}"

    #fullcontent = json.loads(jsoncontent)["body"]
    #print("fc: %s" % fullcontent)
    body_dict = json.loads(jsoncontent.replace("'", "\""))
    #body_dict = fullcontent
    print(body_dict)
    for x in body_dict:
        print("%s: %s" % (x, body_dict[x]))

    #print(body_dict['payload']['user'])

    try:
        jsonschema.validate(body_dict, schema)
        sys.stdout.write("Record #{}: OK\n".format(body_dict))
    except jsonschema.exceptions.ValidationError as ve:
        sys.stderr.write("Record #{}: ERROR\n".format(body_dict))
        sys.stderr.write(str(ve.message) + "\n")

if __name__ == '__main__':
    loadJson()