"""
    TODO: Добавить ассоциацию статусов с исключениями.
    К примеру:
        - errorcodes.UNIQUE_VIOLATION: UniqueViolation
        - errorcodes.FOREIGN_KEY_VIOLATION: ForeignKeyViolation
        - errorcodes.CHECK_VIOLATION: CheckViolation

    Для того, что бы подключить его в декораторе handle_exception.
    Все ассоциации должны быть в app/internal/pkg/models/exceptions/association/aiopg.py
"""
