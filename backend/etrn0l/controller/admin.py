from flask import request, jsonify
from flask_controller import FlaskController, route  # type: ignore
from marshmallow import ValidationError
from ..service import FlashLoopService
from ..schema import FlashLoopRequestSchema
from ..util import ApiResponse


@route("/api/v1/admin")
class AdminController(FlaskController):
    """Exposes a rest interface for administrating the site."""
    def __init__(self, flash_loop_service: FlashLoopService):
        super().__init__()
        self.flash_loops = flash_loop_service

    @route("/loops", methods=["POST"])
    def post_loops(self):
        json = request.get_json()

        try:
            loop = FlashLoopRequestSchema().load(json)
        except ValidationError:
            return jsonify(ApiResponse.bad_request()), 400

        id = self.flash_loops.add_loop(loop)
        return jsonify(ApiResponse.ok({"id": id})), 200

    @route("/loops/<id>", methods=["GET"])
    def get_loop(self, id):
        loop = self.flash_loops.get_loop_by_id(id)

        if (loop is not None):
            return jsonify(loop)

        jsonify({"nope": 404})
