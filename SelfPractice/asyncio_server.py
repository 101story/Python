import asyncio


async def run_server():
    server = await asyncio.start_server(handler, host="127.0.0.1", port=7001)
    async with server:
        # 클라이언트와 연결을 수락
        await server.serve_forever()

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # 클라이언드로부터 데이터 받기
    data: bytes = await reader.read(1024)
    peername = writer.get_extra_info('peername')
    print(f" {peername} sent {len(data)} bytes ")
    msg = data.decode()
    print(msg)
    # 클라이언트에게 다시 메시지보내기
    res = msg[::-1]
    writer.write(res.encode())
    await writer.drain()

async def test():
    await asyncio.wait([run_server()])

if __name__ == "__main__":
    asyncio.run(test(), debug=True)