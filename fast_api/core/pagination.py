from fastapi.params import Query

from core.config import configs


class PaginatedParams:
    def __init__(self,
                 page_number: int = Query(configs.cfg.default_page_number, gt=0, le=100),
                 page_size: int = Query(configs.cfg.default_page_size, gt=0, le=100)
    ):
        self.page_number = page_number
        self.page_size = page_size