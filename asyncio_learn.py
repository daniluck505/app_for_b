import asyncio


async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'{count} second have passed')
        count += 1
        await asyncio.sleep(1)


async def main():
    # создаем задачи в событийном цикле
    # task1 = asyncio.ensure_future(print_nums())
    # task2 = asyncio.ensure_future(print_time ())
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    # создаем цикл
    # loop = asyncio.get_event_loop()
    # запускаем цикл до завершения работы функций внутри
    # loop.run_until_complete(main())
    # закрываем цикл
    # loop.close()

    asyncio.run(main())