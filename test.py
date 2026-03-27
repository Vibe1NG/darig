from ruamel.yaml import YAML

yaml = YAML(typ="rt")
text = '{\n  "a": 1\n}'

try:
    for doc in yaml.load_all(text):
        print(getattr(doc, "lc", None))
except Exception as e:
    print(e)
