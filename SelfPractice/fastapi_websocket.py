from fastapi import WebSocket
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat And File Download Client</title>
    <script type="text/javascript">

        var ws = null;

        function sendTestConnect() {
            ws = new WebSocket("ws://localhost:8000/ws");

            ws.onopen=function(){
                alert("연결 완료");
            };

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            }

            ws.onclose = function(e) {
                alert(e.msg);
            };

            ws.onerror = function(e) {
                alert(e.msg);
            }
        }

        function saveFile(blob) {
              var link = document.createElement('a');
              link.href = window.URL.createObjectURL(blob);
              link.download = 'ws_file.xlsx';
              link.click();
        };

        function sendFileConnector(){

            var url = "ws://localhost:8000/ws_file";
            ws = new WebSocket(url);

            ws.binaryType="arraybuffer";
            ws.onopen=function(){
                alert("연결 완료");
            };

            ws.onmessage = function(e){
                // 파일은 ArrayBuffer 로 온다
                // e.data 의 type 은 ArrayBuffer 이고 이것을 DataView 로 넘겨준다.
                var dataView = new DataView(e.data);
                // DataView 를 넘겨줘서 Blob 형태로 만들고
                var blob = new Blob([dataView]);
                // blob 를 파일로 저장한다.
                saveFile(blob);
            };

            ws.onclose = function(e) {
                alert(e.msg);
            };
            ws.onerror = function(e) {
                alert(e.msg);
            }
        }

        function requestFile(){
            // 테스트용 파일을 다운로드 요청
            ws.send("fileName:ws_file.xlsx");
        }

        function addEvent(){
            document.getElementById("connect").addEventListener("click", sendTestConnect, false);
            document.getElementById("messageText").addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            });
            document.getElementById("connectFile").addEventListener("click", sendFileConnector, false);
            document.getElementById("sendFile").addEventListener("click", requestFile, false);
        }

        window.addEventListener("load", addEvent, false);
    </script>

</head>

    <body>
        <h1>WebSocket Chat</h1>
        <input id="connect" type="button" value="connect"> <br>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        </script>

        <h1>WebSocket File</h1>
        <input id="connectFile" type="button" value="connect">
        <input id="sendFile" type="button" value="start download">

    </body>
</html>
"""
# [출처] [JAVA / JAVASCRIPT] WebSocket 파일 다운로드|작성자 kf80s


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@app.websocket("/ws_file")
async def websocket_endpoint(websocket: WebSocket):
    print("started")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"received: {data}")
            bytes_data = open("test_openpyxl.xlsx", "rb")
            await websocket.send_bytes(bytes_data)
            print("sent")
            bytes_data.close()
    except Exception as e:
        print(e)
    finally:
        await websocket.close()

# pip install fastapi
# pip install websockets
# pip install "uvicorn[standard]"
# uvicorn fastapi_websocket:app --reload
