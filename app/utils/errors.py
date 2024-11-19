import traceback
from typing import Tuple
from flask import Response, jsonify
from app.utils.logger import Logger

class Errors:
    logger = Logger()

    @staticmethod
    def handle_errors(message: str, exception: Exception, status_code: int, context: str = "") -> Tuple[Response, int]:
        """Handles an error by logging it and returning a JSON error response."""
        Errors.logger.add_to_log("error", f"{message}: {exception}")
        Errors.logger.add_to_log("error", traceback.format_exc())
        if context:
            Errors.logger.add_to_log("error", f"Context: {context}")

        # Return a standardized JSON error response
        error_response = jsonify({
            'message': message,
            'success': False,
            'context': context
        })
        return error_response, status_code
