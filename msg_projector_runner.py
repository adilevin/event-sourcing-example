import msg_factory

_, MSG_PROJECTOR, _, _ = msg_factory.create_msg_cqrs(prod_config=True)

MSG_PROJECTOR.run_infinite_refresh_loop(seconds_to_sleep=1.0, max_num_events_to_process=10)
