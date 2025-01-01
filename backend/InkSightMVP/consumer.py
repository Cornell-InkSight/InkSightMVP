import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LivestreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.room_group_name = "livestream_group"

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        video_chunk = data.get("video_chunk")

        result = await self.process_video_chunk(video_chunk)

        await self.send(text_data=json.dumps({
            "result": result
        }))

    async def process_video_chunk(self, video_chunk):
        return "Processed frame data"
