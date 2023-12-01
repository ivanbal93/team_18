def pagination_params(
    limit: int = 10,
    skip: int = 0
):
    return {"limit": limit, "skip": skip}
