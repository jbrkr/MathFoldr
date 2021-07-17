from api.feature_extraction import trigger
from fileaccess import datasets as fileaccess_datasets
from dataaccess.types import PermissionType
from api.errors import AccessDeniedError
from dataaccess import tokens as dataaccess_tokens
from dataaccess import documents as dataaccess_documents
from dataaccess import datasets as dataaccess_datasets
from api.data_models import DatasetCreate, DatasetUpdate, Pagination
from api.auth import Auth, OptionalAuth
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import os
import io
import pandas as pd
from fastapi import APIRouter, Path, Query, Depends, File
from starlette.responses import FileResponse
from urllib.parse import urlparse

import nltk

nltk.download('averaged_perceptron_tagger')


router = APIRouter()


@router.get(
    "/docs",
    tags=["docs"],
    summary="Get list of docs",
    description="Get list of docs"
)
async def docs_index(
        q: str = Query(None, description="An optional search query"),
        pagination: Pagination = Depends(),
        auth: OptionalAuth = Depends()
):
    return await dataaccess_datasets.browse(
        q=q,
        page_number=pagination.page_number,
        page_size=pagination.page_size
    )


@router.post(
    "/docs",
    tags=["docs"],
    summary="Create a new doc",
    description="Create a new doc using the provided metadata.",
    response_description="The created doc"
)
async def docs_create(
        doc: docCreate,
        auth: Auth = Depends()
):
    # Create dataset
    doc_db = await dataaccess_datasets.create(
        title=docs.title,
        dataset=docs.dataset
    )

    # Assign the user to the dataset
    project_user_db = await dataaccess_datasets.create_dataset_user(
        id=doc_db["id"],
        # user_id=auth.user_id,
        # permission_type=PermissionType.owner
        )

    return dataset_db


@router.put(
    "/docs/{id}",
    tags=["docs"],
    summary="Update doc information",
    description="Update doc information",
    response_description="The doc information"
)
async def docs_update(
        dataset: docsUpdate,
        id: int = Path(..., description="The dataset id"),
        # auth: Auth = Depends()
):
    # Update
    docs_db = await dataaccess_datasets.update(
        id=id,
        title=dataset.title,
        dataset=docs.dataset
    )

    return dataset_db


@router.get(
    "/docs/{id}",
    tags=["docs"],
    summary="Get information about a doc",
    description="Get all information about a specific doc.",
    response_description="The doc"
)
async def datasets_fetch(
        id: int = Path(..., description="The doc id")
):
    result = await dataaccess_datasets.get(id)

    return result


@router.post(
    "/docs/{id}/upload",
    tags=["docs"],
    summary="Upload a zip file of documents",
    description="Upload a zip file of documents"
)
async def datasets_upload_with_id(
        file: bytes = File(...),
        id: int = Path(..., description="The docs id"),
        # auth: Auth = Depends()
):
    print(len(file), type(file))

    # Get dataset details
    dataset = await dataaccess_datasets.get(id)

    # Save/Extract the file
    document_list = fileaccess_datasets.save_extract_dataset(file, str(id))

#    for document_path in document_list:
#        print("Saving document:", document_path)
#
#        # Read the document
#        with open(document_path) as f:
#            document = f.read()
#
#            # Save Document into DB
#            document_db = await dataaccess_documents.create(
#                dataset_id=id,
#                document_name=os.path.basename(document_path),
#                filepath=document_path,
#                document_text=document
#            )
#
#            # Generate sentences
#            sentences = sent_tokenize(document)
#
#            # Tokenize document content
#            tokens = []
#            for s_idx, s in enumerate(sentences):
#                words = word_tokenize(s)
#                pos_tags = pos_tag(words)
#
#                for w_idx, w in enumerate(words):
#                    # Save tokens
#                    token_db = await dataaccess_tokens.create(
#                        document_id=document_db["id"],
#                        sentence_id=s_idx,
#                        token_id=w_idx,
#                        token_text=w,
#                        token_pos_tag=pos_tags[w_idx][1]
#                    )

    # Preprocessing Trigger for parsers

    # trigger.preprocesses_entities(id)


@router.delete(
    "/docs/{id}",
    tags=["docs"],
    summary="Delete a doc",
    description="Delete a doc"
)
async def docs_delete(
    id: int = Path(..., description="The doc id"),
    auth: Auth = Depends()
):
    await dataaccess_datasets.delete(
        id=id
    )
