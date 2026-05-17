import logging
import os
import pickle
from typing import Any, Dict, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


logger = logging.getLogger("generation_mardi_google_docs")

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def authenticate_google(credentials_path: str, token_path: str) -> Any:
    creds = None
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.isfile(credentials_path):
                raise FileNotFoundError(f"Fichier Google credentials introuvable : {credentials_path}")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("docs", "v1", credentials=creds)


def create_google_doc(service: Any, title: str) -> str:
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId")
    if not doc_id:
        raise RuntimeError("Google Docs n'a pas retourné de documentId.")
    logger.info("Document Google Docs créé : %s", doc_id)
    return doc_id


def build_doc_content(course_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    requests = []
    index = 1

    title = course_json.get("title", "Formation - Géométrie analytique")
    requests.append(
        {
            "insertText": {
                "location": {"index": index},
                "text": title + "\n",
            }
        }
    )
    requests.append(
        {
            "updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + len(title)},
                "paragraphStyle": {"namedStyleType": "TITLE"},
                "fields": "namedStyleType",
            }
        }
    )
    index += len(title) + 1

    intro = course_json.get("description", "")
    if intro:
        requests.append(
            {
                "insertText": {
                    "location": {"index": index},
                    "text": intro + "\n\n",
                }
            }
        )
        index += len(intro) + 2

    for chapter in course_json.get("chapters", []):
        chapter_title = chapter.get("title", "Chapitre")
        requests.append(
            {
                "insertText": {
                    "location": {"index": index},
                    "text": chapter_title + "\n",
                }
            }
        )
        requests.append(
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": index, "endIndex": index + len(chapter_title)},
                    "paragraphStyle": {"namedStyleType": "HEADING_1"},
                    "fields": "namedStyleType",
                }
            }
        )
        index += len(chapter_title) + 1

        content = chapter.get("content", "")
        if content:
            requests.append(
                {
                    "insertText": {
                        "location": {"index": index},
                        "text": content + "\n\n",
                    }
                }
            )
            index += len(content) + 2

        quiz = chapter.get("quiz", [])
        if quiz:
            requests.append(
                {
                    "insertText": {
                        "location": {"index": index},
                        "text": "Mini quiz\n",
                    }
                }
            )
            requests.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": index + 9},
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType",
                    }
                }
            )
            index += 10

            for question_index, question in enumerate(quiz, start=1):
                question_text = f"Question {question_index}: {question.get('question', '')}\n"
                requests.append(
                    {
                        "insertText": {
                            "location": {"index": index},
                            "text": question_text,
                        }
                    }
                )
                index += len(question_text)

                for choice in question.get("choices", []):
                    choice_text = f"• {choice}\n"
                    requests.append(
                        {
                            "insertText": {
                                "location": {"index": index},
                                "text": choice_text,
                            }
                        }
                    )
                    index += len(choice_text)

                answer = f"Bonne réponse : {question.get('answer', '')}\n"
                requests.append(
                    {
                        "insertText": {
                            "location": {"index": index},
                            "text": answer,
                        }
                    }
                )
                index += len(answer)

                explanation = f"Explication : {question.get('explanation', '')}\n\n"
                requests.append(
                    {
                        "insertText": {
                            "location": {"index": index},
                            "text": explanation,
                        }
                    }
                )
                index += len(explanation)

    return requests


def create_google_docs_formation(
    course_json: Dict[str, Any],
    credentials_path: str,
    token_path: str,
    document_title: str,
) -> str:
    service = authenticate_google(credentials_path, token_path)
    doc_id = create_google_doc(service, document_title)

    requests = build_doc_content(course_json)
    service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    logger.info("Document Google Docs créé : %s", doc_url)
    return doc_url
