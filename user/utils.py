from django.conf import settings
from utils.communication import (
    send_mail_using_smtp,
    get_mail_template,
)
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from user.models import ModulePermission, User


def send_email(instance, password):
    login_link = f"{settings.FRONT_END_URL}/auth/signin"
    email_data = {
        "from": settings.EMAIL_HOST_USER,
        "subject": "Legal Portal Credentials",
        "message": get_mail_template(
            "login_credentials",
            {
                "name": instance.first_name + " " + instance.last_name,
                "email": instance.email,
                "password": password,
                "login_link": login_link,
            },
        ),
        "recipient": [instance.email],
    }
    send_mail_using_smtp(email_data)


def arrange_permissions(permissions: list):
    module_map = {
        "case": "Case",
        "profile": "Employee_Management",
        "practicearea": "Practice_Area",
        "client": "Client",
        "task": "Task",
        "media": "Document",
    }
    converted_permissions = []
    for permission in permissions:
        permission_name = permission.split(".")[1]
        module_name = permission.split(".")[0]
        model_name = permission.split("_")[1]
        mapped_module = module_map.get(model_name, module_name.capitalize())

        existing_module = next(
            (
                perm
                for perm in converted_permissions
                if perm["module"].lower() == mapped_module.lower()
            ),
            None,
        )
        if not existing_module:
            if permission_name.startswith("view"):
                converted_permissions.append(
                    {"module": mapped_module, "access_level": "r"}
                )
            elif permission_name.startswith(("delete", "change", "add")):
                converted_permissions.append(
                    {"module": mapped_module, "access_level": "w"}
                )
        else:
            if existing_module["access_level"] == "w":
                pass
            else:
                if permission_name.startswith(("delete", "change", "add")):
                    existing_module["access_level"] = "w"
                elif permission_name.startswith("view"):
                    existing_module["access_level"] = "r"
    return converted_permissions


def assign_permissions(group_or_user, permissions):
    if isinstance(group_or_user, Group):
        group_or_user.permissions.clear()
    elif isinstance(group_or_user, User):
        remove_all_permissions(group_or_user)
    else:
        raise ValueError("Invalid object type. Expected User or Group.")

    for permission in permissions:
        if not permission["module"] or not permission["access_level"]:
            raise AttributeError("Invalid permission data")
        module = permission["module"]
        perm = permission["access_level"]
        if not ModulePermission.objects.filter(module=module.lower()).exists():
            continue
        if perm.lower() not in ["r", "w"]:
            raise ValueError("Invalid permissions")
        if perm.lower() == "r":
            module_permission = ModulePermission.objects.get(
                module=module.lower()
            ).permission.get("R")
            read_perms = list(Permission.objects.filter(id__in=module_permission))
            if isinstance(group_or_user, Group):
                group_or_user.permissions.add(*read_perms)
            else:
                group_or_user.user_permissions.add(*read_perms)
        elif perm.lower() == "w":
            module_permission = ModulePermission.objects.get(
                module=module.lower()
            ).permission.get("W")
            write_perms = Permission.objects.filter(id__in=module_permission)
            if isinstance(group_or_user, Group):
                group_or_user.permissions.add(*write_perms)
            else:
                group_or_user.user_permissions.add(*write_perms)
    return convert_into_permission_list(group_or_user)


def convert_into_permission_list(group_or_user):
    if isinstance(group_or_user, Group):
        group_permissions = {
            f"{perm.content_type.app_label}.{perm.codename}"
            for perm in group_or_user.permissions.all()
        }
        return group_permissions
    return group_or_user.get_all_permissions()


def assign_permissions_to_employee(user, permissions):
    assigned = False
    for perm in permissions:
        if not isinstance(perm, dict):
            raise ValueError("Invalid permissions format")
        if "group" in list(perm.keys())[0].lower():
            remove_all_permissions(user)
            group_id = perm[list(perm.keys())[0]]
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
            assigned = True
            break
    if not assigned:
        assign_permissions(user, permissions)
    return


def remove_all_permissions(user):
    user.role = 3
    user.is_staff = False
    user.groups.clear()
    user.user_permissions.clear()
    user.save()


def create_search_clauses(filter_field, filter_value):
    if filter_field == "name":
        return Q(first_name__icontains=filter_value) | Q(
            last_name__icontains=filter_value
        )
    elif filter_field == "group":
        return Q(user__groups__name__icontains=filter_value)
    else:
        return Q(**{f"{filter_field}__icontains": filter_value})
