# Twilio Media Stream with ngrok (Example)

## 1) Start server
```bash
uvicorn app.main:app --reload
```

## 2) Start ngrok
```bash
ngrok http 8000
```

## 3) Configure Twilio
- Voice webhook: `https://<ngrok-id>.ngrok-free.app/twilio/voice`
- Stream URL: `wss://<ngrok-id>.ngrok-free.app/twilio/stream`

## 4) Place a test call
- Twilio will connect to your `/twilio/voice` endpoint and open the media stream.
