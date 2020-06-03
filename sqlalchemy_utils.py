import sqlachemy as sa
from sqlalchemy.sql import func
from sqlachemy.dialects import postgresql as pg


def pk(*foreign_key_column_names):
    """A UUID primary key.
    Return a standard primary key of type UUID for use in models. If the
    any foreign_key_column_names are supplied, the primary key will
    reference the given columns.
    :param foreign_key_column_names: column names of the referenced foreign
                                    keys (should be 'table_name.column_name')
    :return: a SQLAlchemy Column for a UUID primary key.
    """
    args = [pg.UUID]
    args.extend(map(fk, foreign_key_column_names))
    kwargs = {
        'primary_key': True,
        'server_default': func.uuid_generate_v4(),
    }
    return sa.Column(*args, **kwargs)


def fk(column_name):
    """A foreign key with ONUPDATE CASCADE and ONDELETE CASCADE.
    Return a foreign key of type UUID for use in models.
    The relationship CASCADEs on UPDATE and DELETE.
    :param column_name: the name of the referenced column
    :return: a SQLAlchemy Column for a UUID primary key.
    """
    return sa.ForeignKey(column_name, onupdate='CASCADE', ondelete='CASCADE')


def last_update_time():
    """A timestamp column set to CURRENT_TIMESTAMP on update.
    Return a column containing the time that a record was last updated.
    :return: a SQLAlchemy Column for a datetime with time zone auto-updating
             column
    """
    return sa.Column(
        pg.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=current_timestamp(),
        onupdate=current_timestamp(),
    )


def json_column(column_name, *, default=None):
    """A JSONB column.
    Return a column of type JSONB for use in models. Use this for entries like
        <language>: <text>
    :param column_name: the name of the column
    :param default: the column default (default value None, meaning no column
                    default)
    :return: a SQLAlchemy Column for a non-null JSONB type.
    """
    return sa.Column(
        pg.json.JSONB,
        sa.CheckConstraint(
            "{} @> '{{}}'".format(column_name),
            name='{}_valid_json_check'.format(column_name),
        ),
        nullable=False,
        server_default=default,
    )


def last_update_time():
    """A timestamp column set to CURRENT_TIMESTAMP on update.
    Return a column containing the time that a record was last updated.
    :return: a SQLAlchemy Column for a datetime with time zone auto-updating
             column
    """
    return sa.Column(
        pg.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=current_timestamp(),
        onupdate=current_timestamp(),
    )


def get_model(session, model_cls, model_id, exception=None):
    """Throw an error if session.query.get(model_id) returns None."""
    model = session.query(model_cls).get(model_id)
    if model is None:
        if exception is None:
            exception = NoResultFound((model_cls, model_id))
        raise exception
    return model


def _get_field(model, field_name):
    model_dict = model._asdict()
    try:
        return model_dict[field_name]
    except KeyError:
        return getattr(model, field_name)


def get_fields_subset(model: Base, fields):
    """Return the given fields for the model's dictionary representation."""
    return OrderedDict(
        (name, _get_field(model, name)) for name in fields if name
    )


def column_search(query, *,
                  model_cls, column_name, search_term,
                  language=None, regex=False):
    """Modify a query to search a column's values (JSONB or TEXT).
    TODO: document this
    :param query: a
    :param model_cls: aa
    :param column: b
    :param search_term: c
    :param language: d
    :param regex: r
    :return: The modified query.
    """
    column = getattr(model_cls, column_name)
    if not regex:
        search_term = search_term.translate(str.maketrans(
            {'%': '\%', '_': '\_', '\\': r'\\'}
        ))
    # JSONB column
    if str(column.type) == 'JSONB':
        if language is None:
            # note that Node has no default_language
            language = model_cls.default_language
        # Search for a specific language
        if regex:
            return (
                query
                .filter(sa.text("{}->>:lang ~* :search_term".format(column)))
                .params(lang=language, search_term=search_term)
            )
        return (
            query
            .filter(column[language].astext.ilike('%{}%'.format(search_term)))
        )

    # TEXT column
    if regex:
        return (
            query
            .filter(sa.text('{} ~* :search_term'.format(column)))
            .params(search_term=search_term)
        )
    return (
        query
        .filter(column.ilike('%{}%'.format(search_term)))
    )
