#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta

from yapapi import Golem
from yapapi.services import Service
from yapapi.log import enable_default_logger
from yapapi.payload import vm

REFRESH_INTERVAL_SEC = 5


class ShardService(Service):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash="d646d7b93083d817846c2ae5c62c72ca0507782385a2e29291a3d376",
            min_mem_gib=4,
            min_storage_gib=16.0,
        )

    async def start(self):
        self._ctx.run()
        yield self._ctx.commit()

    async def run(self):
        while True:
            await asyncio.sleep(REFRESH_INTERVAL_SEC)
            self._ctx.run()

            future_results = yield self._ctx.commit()
            results = await future_results
            print(results[0].stdout.strip())


async def main():
    async with Golem(budget=1.0, subnet_tag="devnet-beta.2") as golem:
        cluster = await golem.run_service(ShardService, num_instances=1)
        start_time = datetime.now()

        while datetime.now() < start_time + timedelta(minutes=1):
            for num, instance in enumerate(cluster.instances):
                print(f"Instance {num} is {instance.state.value} on {instance.provider_name}")
            await asyncio.sleep(REFRESH_INTERVAL_SEC)


if __name__ == "__main__":
    enable_default_logger(log_file="hello.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)