from utils.base_query_params import get_selector
from rest_framework.serializers import ValidationError
from django.db.models import Lookup, JSONField
from django.contrib.contenttypes.models import ContentType


def get_selector_from_body(self, key, required=True):
    if not required:
        return self.request.data.get(key, None)
    value = self.request.data.get(key)
    if not value:
        raise KeyError(f"{key} is required")
    return value


def get_selector_from_query_param(self, key, required=False):
    if not required:
        return self.request.GET.get(key, None) or self.request.query_params.get(
            key, None
        )
    value = self.request.GET.get(key, None) or self.request.query_params.get(key, None)
    if not value:
        raise KeyError(f"{key} is required")
    return value


def get_filter_clauses(self, filter_fields, create_filter_clause):
    filter_clauses = []
    for filter_field in filter_fields:
        filter_value = get_selector(self, filter_field)
        if filter_value:
            filter_clause = create_filter_clause(
                filter_field,
                filter_value,
            )
            filter_clauses.append(filter_clause)
    return filter_clauses


def get_enum_choices(class_name):
    return [(key.value, key.name) for key in class_name]


def check_positive_int(value):
    if value < 0:
        raise ValidationError("Values must be positive")


class JSONBPartialMatch(Lookup):
    lookup_name = "jsonb_partial_match"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        key, search_value = rhs_params[0]

        sql = f"""
        EXISTS (
            SELECT 1 FROM jsonb_array_elements({lhs}) data
            WHERE data->>%s ILIKE %s
        )
        """
        return sql, lhs_params + [key, f"%{search_value}%"]


JSONField.register_lookup(JSONBPartialMatch)


def get_content_type_for_model(model):
    return ContentType.objects.get_for_model(model)
