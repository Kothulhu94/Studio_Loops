# Last Errors

### concept_producer (2026-05-13T02:55:15.793254)
MODEL_TRANSPORT_ERROR at stage 'concept_producer': KoboldCPP transport failure at http://127.0.0.1:5001/v1/chat/completions: HTTPConnectionPool(host='127.0.0.1', port=5001): Max retries exceeded with url: /v1/chat/completions (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=5001): Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it")). Configured timeout=(connect=15s, read=1800s).. KoboldCPP timed out, disconnected, or returned an unusable client response before ACTIONS_JSON could be parsed. No schema repair was attempted because this was not model output.

