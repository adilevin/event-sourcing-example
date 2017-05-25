import msg_factory

CMD_HANDLER, _, _, QUERY_HANDLER = msg_factory.create_msg_cqrs(
    prod_config=True, reset=True)

raw_input("Press Enter to send messages...")

for i in range(3):
    print " Sending 4 messages to user%d" % i
    for j in range(4):
        CMD_HANDLER.send_msg_to_user("user%d" % i, "msg%d%d" % (i, j))

raw_input("Press Enter to mark messages as read...")

for i in range(2):
    print " Marking 2 messages read for user%d" % i
    for j in range(2):
        CMD_HANDLER.mark_msg_as_read("user%d" % i, "msg%d%d" % (i, j))

print "Use CMD_HANDLER and QUERY_HANDLER"
