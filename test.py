import coreapi

# Initialize a client & load the schema document
client = coreapi.Client()
schema = client.get("http://127.0.0.1:8000/docs/")

# Interact with the API endpoint
action = ["users", "demo > list"]
result = client.action(schema, action)

["hbp_1", "hbp_4", "hbp_2", "hbp_3", "ok139_3", "hbp_8", "ok139_2", "hbp_5", "ftx_152", "ba_2"]