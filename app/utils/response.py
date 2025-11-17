def api_success(data, message="OK", code="200", pagination=None):
    return {
        "data": data,
        "meta": {
            "message": message,
            "status": "success",
            "code": code,
            "pagination": pagination
        }
    }


def api_error(message="Error", code="400"):
    return {
        "data": None,
        "meta": {
            "message": message,
            "status": "error",
            "code": code
        }
    }


def build_pagination(page: int, limit: int, total: int):
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }
