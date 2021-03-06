from flask import request, jsonify
from flask_controller import FlaskController, route  # type: ignore
from marshmallow import ValidationError
from ..service import FlashLoopService, FlashFileService
from ..schema import FlashLoopRequestSchema
from ..ext import ApiResponse


@route("/api/v1/admin")
class AdminController(FlaskController):
    """Exposes a rest interface for administrating the site."""

    def __init__(self,
                 flash_loop_service: FlashLoopService,
                 flash_file_service: FlashFileService):
        super().__init__()
        self.flash_loops = flash_loop_service
        self.flash_files = flash_file_service

    @route("/loops", methods=["GET"])
    def get_loops(self):
        start = request.args.get("start")

        try:
            if start is not None:
                start = int(start)
            else:
                start = 0
        except ValueError:
            return ApiResponse.bad_request(), 400

        loops = self.flash_loops.list_loops(start, 20)
        count = self.flash_loops.get_loop_count()

        return jsonify(ApiResponse.ok(data=loops, count=count)), 200

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

        if loop is not None:
            return jsonify(ApiResponse.ok(loop)), 200

        return jsonify(ApiResponse.not_found()), 404

    @route("/loops/<id>", methods=["DELETE"])
    def delete_loop(self, id):
        success = self.flash_loops.delete_loop(id)

        if success:
            return jsonify(ApiResponse.ok()), 200

        return jsonify(ApiResponse.not_found()), 404

    @route("/loops/<id>", methods=["PUT"])
    def put_loop(self, id):
        json = request.get_json()

        try:
            loop = FlashLoopRequestSchema().load(json)
        except ValidationError:
            return jsonify(ApiResponse.bad_request()), 400

        loop.id = id
        updated_loop = self.flash_loops.update_loop(loop)

        if updated_loop is None:
            return jsonify(ApiResponse.not_found()), 404

        return jsonify(ApiResponse.ok(updated_loop)), 200

    @route("/loops/<id>/file", methods=["GET"])
    def get_flash_file(self, id):
        url = self.flash_files.get_file(id)

        if url is not None:
            print(url)
            return jsonify(ApiResponse.ok({"url": url})), 200

        return jsonify(ApiResponse.not_found), 404

    @route("/loops/<id>/file", methods=["PUT"])
    def put_flash_file(self, id):
        if "file" in request.files:
            fileobj = request.files["file"].stream
            success = self.flash_files.set_file(id, fileobj)

            if success:
                url = self.flash_files.get_file(id)
                print(url)
                return jsonify(ApiResponse.ok({"url": url})), 200

            return jsonify(ApiResponse.internal_error()), 500

        return jsonify(ApiResponse.bad_request()), 400
