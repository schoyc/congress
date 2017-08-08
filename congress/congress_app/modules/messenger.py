import congress_app.modules.google as google

def respondToMessageEvent(event):
    senderID = event["sender"]["id"]
    recipientID = event["recipient"]["id"]
    timestamp = event["timestamp"]
    message = event["message"]
    nlp_entities = event["nlp"]["entities"]

    messageID = message["mid"]
    messageText = message.get("text")

    if messageText != None:
        if "location" in nlp_entities:
            address = nlp_entities["location"]["value"]
            respondToAddress(address)
        else:
            print(event)

def respondToAddress(address):
    # 1) Translate address to district info w/ Google api
    state, district = google.addressToDistricts(address)

    # 2) TODO: Save district info to user

    # 3) Echo district info back

    # 4) Respond that user has now been subscribed
