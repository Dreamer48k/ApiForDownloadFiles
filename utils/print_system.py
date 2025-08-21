import asyncio
# Заменить на нормальный exception


def debug_console_print(**var):
    """Функция для удобного принта в консоль переменных"""
    for name_var, data_var in var.items():
        print(f'\n{name_var}: {data_var}\n'.format(name_var, data_var))


async def async_debug_console_print(**var):
    """Функция для удобного принта в консоль переменных"""
    for name_var, data_var in var.items():
        await asyncio.sleep(0)
        print(f'\n{name_var}: {data_var}\n'.format(name_var, data_var))
