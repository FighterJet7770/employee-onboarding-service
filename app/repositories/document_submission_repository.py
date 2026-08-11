"""Document submission data-access repository."""

from sqlalchemy.orm import Session

from app.models.document_submission import DocumentStatus, DocumentSubmission


class DocumentSubmissionRepository:
    """Persistence operations for employee documents."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_employee_and_type(self, employee_id: int, document_type: str) -> DocumentSubmission | None:
        return (
            self.db.query(DocumentSubmission)
            .filter(
                DocumentSubmission.employee_id == employee_id,
                DocumentSubmission.document_type == document_type,
            )
            .first()
        )

    def upsert(
        self,
        employee_id: int,
        document_type: str,
        reference_id: str,
        status: DocumentStatus,
    ) -> DocumentSubmission:
        document = self.get_by_employee_and_type(employee_id, document_type)
        if document is None:
            document = DocumentSubmission(
                employee_id=employee_id,
                document_type=document_type,
                reference_id=reference_id,
                status=status,
            )
            self.db.add(document)
        else:
            document.reference_id = reference_id
            document.status = status

        self.db.commit()
        self.db.refresh(document)
        return document
