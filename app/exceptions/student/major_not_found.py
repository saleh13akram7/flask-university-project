class MajorNotFoundError(Exception):

    def __init__(self, major_id: int):
        self.major_id = major_id

        self.message = (
            f"Major with id {major_id} was not found"
        )

        super().__init__(self.message)