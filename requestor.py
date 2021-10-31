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
            image_hash="0a4c65ecfd19a1f45e1f9cf77a2da633fcb22f1dea786c261d26af46",
            min_mem_gib=4,
            min_storage_gib=16.0,
        )

    async def start(self):
        async for script in super().start():
            script = self._ctx.new_script()
            script.run("/bin/mongod", "--dbpath", "/shard/db", "--logpath", "/var/log/mongodb/mongod.log", "-f", "/etc/mongod.conf.orig","--fork")
            print("MongoDB engine started")
            yield script

    async def run(self):
        while True:
            script = self._ctx.new_script()
            script.run("/bin/python3","PyDriver.py", "--create" , str('{"Hello":"world"}'))

            yield script


async def main():
    async with Golem(budget=1.0, subnet_tag="devnet-beta.2") as golem:
        cluster = await golem.run_service(ShardService, num_instances=1)
        start_time = datetime.now()

        while datetime.now() < start_time + timedelta(minutes=1):
            for num, instance in enumerate(cluster.instances):
                print(f"Instance {num} is {instance.state.value} on {instance.provider_name}")
            await asyncio.sleep(REFRESH_INTERVAL_SEC)
            
        cluster.stop()
        while(still_running()):
            await asyncio.sleep(2)

if __name__ == "__main__":
    enable_default_logger(log_file="hello.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)
