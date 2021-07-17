import os
from typing import Any, Dict, List
# from api.auth import Auth, AuthData  # auth.user_id
from dataaccess import utils as data_utils
from dataaccess.session import database
from dataaccess.errors import RecordNotFoundError, NoAccessError
# from dataaccess.types import PermissionType
from fastapi import APIRouter, Path, Query, Depends, File



async def browse(
    *,
    q: str = None,
    page_number: int = 0,
    page_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of rows based on filters
    """

    query = """
        select id, dataset ,title
        from docs
        where 1=1
    """

    if q is not None:
        query += " and (dataset like'%"+q + \
            "%' or title like '%"+q+"%')"

    print("query", query)
    result = await database.fetch_all(query)

    return [prep_data(row) for row in result]


async def get(id: int) -> Dict[str, Any]:
    """
    Retrieve one row based by its id. Return object is a dict. 
    Raises if the record was not found.
    """

    query = """
        select id, dataset ,title
        from docs where id = :id
    """

    values = {
        "id": id
    }

    print("query:", query, "values:", values)
    result = await database.fetch_one(query, values)

    if result is None:
        raise RecordNotFoundError(f"Could not find row with id '{id}'")

    return prep_data(result)


async def create(*,
                 title: str,
                 dataset: str = None,
                 # auth: Auth = Depends(),
                 id: int = None) -> Dict[str, Any]:
    """
    Create a new row. Returns the created record as a dict.
    """

    # Set the values
    values = {
        "title": title,
        # "created_by": AuthData.user_id
    }

    # if the id was passed
    if id is not None:
        values["id"] = id
    if dataset is not None:
        values["dataset"] = dataset

    # Generate the field and values list
    field_list = ", ".join(values.keys())
    param_list = ", ".join(":" + key for key in values.keys())

    result = await database.fetch_one(f"""
        INSERT INTO docs (
            {field_list}
        ) VALUES (
            {param_list}
        ) RETURNING *;
    """, values=values)

    result = prep_data(result)

    return result


async def update(id: int,
                 dataset: str = None,
                 title: str = None,
                 ) -> Dict[str, Any]:
    """
    Updates an existing row. Keyword arguments left at None will not be
    changed in the database. Returns the updated record as a dict. Raises if
    the record was not found.
    """

    values = {
        "id": id
    }

    changes: Dict[str, Any] = {
    }

    if dataset is not None:
        changes["dataset"] = dataset
    if title is not None:
        changes["title"] = title

    change_list = ", ".join(key + " = :" + key for key in changes.keys())
    change_list += ", updated_at = EXTRACT(EPOCH FROM clock_timestamp()) * 1000"

    print(change_list)

    result = await database.fetch_one(f"""
        UPDATE docs
        SET {change_list}
        WHERE id = :id
        RETURNING *;
    """, values={**values, **changes})

    if result is None:
        raise RecordNotFoundError(f"Could not update row with id '{id}'")

    result = prep_data(result)
    return result





async def delete(*, id: int) -> None:
    """
    Deletes an existing row. Raises if the record was not found.
    """

    deleted_row_count = await database.execute("""
        WITH deleted AS (
            DELETE FROM docs
            WHERE id = :id
            RETURNING id
        ) SELECT COUNT(id) FROM deleted;
    """, values={"id": id})

    if deleted_row_count == 0:
        raise RecordNotFoundError(f"Could not delete row with id '{id}'")


def prep_data(result) -> Dict[str, Any]:
    if result is None:
        raise ValueError("Tried to prepare null result")

    result = dict(result)
    return result
