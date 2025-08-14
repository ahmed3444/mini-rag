from enum import Enum
class ResponseStatus( Enum):
    SUCCESS = "success"
    ERROR = "error"
    FILE_IS_NOT_TYPE = "file_is_not_type"
    FILE_SIZE_EXCEEDS_LIMIT = "file_size_exceeds_limit"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    FILE_SAVE_ERROR = "file_save_error"