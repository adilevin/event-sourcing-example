import messages_factory

_, MSGS_PROJECTOR, _, _ = messages_factory.create_messages_cqrs(prod_config=True)

MSGS_PROJECTOR.run_infinite_refresh_loop(seconds_to_sleep=1.0, max_num_events_to_process=10)
