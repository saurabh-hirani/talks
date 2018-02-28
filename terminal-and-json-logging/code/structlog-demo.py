from structlog import get_logger
log = get_logger()
log.info("key_value_logging", out_of_the_box=True, effort=0)

log = log.bind(user="anonymous", some_key=23)
log = log.bind(user="hynek", another_key=42)
log.info("user.logged_in", happy=True)

log = log.unbind('user')

log.info("test")
