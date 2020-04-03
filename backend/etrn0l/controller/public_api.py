from flask import request, jsonify
from flask_controller import FlaskController, route  # type: ignore
from ..service import FlashLoopService
from ..util import ApiResponse


@route("/api/v1")
class PublicApiController(FlaskController):
    """The Public api, meant to be used by the website."""

    def __init__(self, flash_loop_service: FlashLoopService):
        super().__init__()
        self.flash_loops = flash_loop_service

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

    @route("/random", methods=["get"])
    def get_random(self):
        loop = self.flash_loops.get_random_loop()
        loop_count = self.flash_loops.get_loop_count()
        next_loop = self._get_next_loop(loop.number, loop_count)
        prev_loop = self._get_prev_loop(loop.number)

        return jsonify(ApiResponse.ok({
            "loop": loop,
            "next": next_loop,
            "prev": prev_loop
        })), 200

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

        return jsonify(ApiResponse.ok({
            "loop": loop,
            "next": next_loop,
            "prev": prev_loop
        })), 200
