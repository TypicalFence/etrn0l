from flask import request, jsonify
from flask_controller import FlaskController, route  # type: ignore
from ..service import FlashLoopService, FlashFileService
from ..model import FlashLoop
from ..ext import ApiResponse


@route("/api/v1")
class PublicApiController(FlaskController):
    """The Public api, meant to be used by the website."""

    def __init__(self,
                 flash_loop_service: FlashLoopService,
                 flash_file_service: FlashFileService):
        super().__init__()
        self.flash_loops = flash_loop_service
        self.flash_files = flash_file_service

    def _get_next_loop(self, number, max):
        loop = self.flash_loops.get_loop_by_number(number + 1)

        if loop is not None:
            return loop

        if loop is None and number + 1 < max:
            return self._get_next_loop(number + 1, max)

        return None

    def _get_prev_loop(self, number):
        loop = self.flash_loops.get_loop_by_number(number - 1)

        if loop is not None:
            return loop

        if loop is None and number - 1 > 0:
            return self._get_prev_loop(number - 1)

        return None

    def _prepare_loop(self, loop: FlashLoop):
        if loop.id is not None:
            loop.file_url = self.flash_files.get_file(loop.id)

        # strip id
        del loop.id

        return loop

    @route("/random", methods=["get"])
    def get_random_loop_id(self):
        loop = self.flash_loops.get_random_loop()
        return jsonify(ApiResponse.ok({"number": loop.number})), 200

    @route("/loops/<number>", methods=["get"])
    def get_loop(self, number):
        try:
            if number is not None:
                number = int(number)
            else:
                number = 0
        except ValueError:
            return jsonify(ApiResponse.not_found())

        loop = self.flash_loops.get_loop_by_number(number)

        if loop is None:
            return jsonify(ApiResponse.not_found())

        loop_count = self.flash_loops.get_loop_count()
        next_loop = self._get_next_loop(loop.number, loop_count)
        prev_loop = self._get_prev_loop(loop.number)

        if next_loop is not None:
            next_loop = next_loop.number

        if prev_loop is not None:
            prev_loop = prev_loop.number

        return jsonify(ApiResponse.ok({
            "loop": self._prepare_loop(loop),
            "next": next_loop,
            "prev": prev_loop
        })), 200

    @route("/loops/random", methods=["get"])
    def get_random_loop(self):
        loop = self.flash_loops.get_random_loop()
        return self.get_loop(loop.number)
