from ctypes import Union
from typing import Type, Optional, List

from tortoise import Model
from tortoise.query_utils import Prefetch
from tortoise.queryset import QuerySet


def _generate_query(
        query: QuerySet,
        prefetch_related: bool,
) -> QuerySet:
    if prefetch_related:
        if prefetch_related is True:
            prefetch_related = [*query.model._meta.fetch_fields]

        return query.prefetch_related(*prefetch_related)

    return query

async def paginate(
        query: QuerySet,
        page_size: Optional[int] = 10,
        page: Optional[int] = 1,
        prefetch_related: bool = False,
):
    if not isinstance(query, QuerySet):
        query = query.all()

    if page_size == 0:
        page_size = 10
    if page != 0:
        page -= 1

    total = await query.count()

    items = (
        await _generate_query(query, prefetch_related).order_by('created_at')
        .offset(page_size * page)
        .limit(page_size)
        .all()
    )

    return items, total

def uuid2str(uuid_data):
    return str(uuid_data) if uuid_data else None