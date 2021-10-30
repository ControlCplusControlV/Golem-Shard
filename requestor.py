import asyncio
from datetime import datetime, timedelta

from yapapi import Golem
from yapapi.services import Service
from yapapi.log import enable_default_logger
from yapapi.payload import vm



class ShardService(Service):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash="9d8f86823b6864975f87ad0f8c5a879574c7b192b99804dcb123ad0b",
            min_mem_gib=4,
            min_storage_gib=16.0,
        )

    async def start(self):
        self._ctx.run("/bin/sh", "mongod", "--dbpath", "/shard/db", "--logpath", "/var/log/mongodb/mongod.log", "--fork")
        self._ctx.run("/bin/sh", "mongo", "mongoScript.js")
        initialize = yield self._ctx.commit()
        await initialize

    async def run(self):
        while True:
            self._ctx.run("PyDriver.py", "--create" , str('{"Hello":"world"}'))

            future_results = yield self._ctx.commit()
            results = await future_results


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
