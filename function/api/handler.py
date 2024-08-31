from jinja2 import Template
import json

def handle(req):
    input = json.loads(req)

    t = Template("{{greeting}} {{name}}")
    res = t.render(name=input["name"], greeting=input["greeting"])
    return res


# def handle(req):
#     """handle a request to the function
#     Args:
#         req (str): request body
#     """
#     return "HELLO WORLD"
#     # return "Input: {}".format(req)

#     return req
