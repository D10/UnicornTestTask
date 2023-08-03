

class FakeRequest:

    def __init__(
            self,
            body=None,
            match_info=None
    ):
        if match_info is None:
            match_info = {}
        if body is None:
            body = {}

        self.body = body
        self.match_info = match_info
        self.body_exists = bool(body)

    async def json(self):
        return self.body


