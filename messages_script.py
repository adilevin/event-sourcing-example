import messages_factory

CMD_HANDLER, _, _, _ = messages_factory.create_messages_cqrs(
    prod_config=True, reset=True)

for i in range(10):
    print "Sending message to user%d" % i
    for j in range(5):
        CMD_HANDLER.send_message_to_user("user%d" % i, "msg%d%d" % (i, j))
