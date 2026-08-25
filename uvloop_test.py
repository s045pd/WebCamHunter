import asyncio
from dataclasses import dataclass

import httpx
import pandas as pd
import uvloop


@dataclass()
class worker:
    datas = pd.read_csv("cam.csv")
    conns = 20
    timeout = 5
    stack_size = 1000

    async def check_one(self, item):
        _, ip, port, auth_str, *_ = item[1]
        auth = tuple(auth_str.split(":"))
        url = f"http://{ip}:{port}"
        try:
            async with httpx.AsyncClient(
                http2=True, verify=False, timeout=self.timeout
            ) as client:
                resp = await client.head(url, auth=httpx.BasicAuth(*auth))
                print(ip, port, auth,resp.headers)
        except Exception as e:
            print(e)

    
    async def run_all(self):
        stack = []
        n = 0
        for item in self.datas.iterrows():
            if n >1000:
                return 
            else:
                n+=1
            if str(item[1][4]).strip().lower() == "hipcam":
                task = asyncio.create_task(self.check_one(item))
                if len(stack) < self.stack_size:
                    stack.append(task)
                else:
                    await asyncio.gather(*stack)
                    stack = [task]
        await asyncio.gather(*stack)

    def main(self):
        asyncio.run(self.run_all())


if __name__ == "__main__":
    worker().main()
