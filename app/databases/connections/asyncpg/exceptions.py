from utils.print_system import debug_console_print


class WaitFreeConnectionTimeoutError(TimeoutError):
    debug_console_print('asyncpg_ERROR_CONNECTION', 'TimeoutError')
    # pass
