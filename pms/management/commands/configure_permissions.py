from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from user.models import ModulePermission


class Command(BaseCommand):
    def handle(self, *args, **options):
        module_map = {
            "user": "User",
        }
        app_name = ["user"]
        model_name = ["user"]

        content_type_ids = {}
        data = None
        if model_name:
            for model in model_name:
                content_types = ContentType.objects.filter(model=model.lower())
                content_type_ids.update({model: [ct.id for ct in content_types]})
        if app_name:
            for app in app_name:
                content_types = ContentType.objects.filter(app_label=app)
                content_type_ids.update(
                    {app: [ct.id for ct in content_types]}
                )
        for key, value_list in content_type_ids.items():
            view_permission_ids = []
            all_permission_ids = []
            for content_type_id in value_list:
                permissions = Permission.objects.filter(content_type=content_type_id)
                for perm in permissions:
                    all_permission_ids.append(perm.id)

                    if "view" in perm.codename:
                        view_permission_ids.append(perm.id)

                data = {"R": view_permission_ids, "W": all_permission_ids}
            if ModulePermission.objects.filter(module=module_map[key].lower()).exists():
                ModulePermission.objects.filter(module=module_map[key].lower()).update(
                    permission=data
                )
            else:
                ModulePermission.objects.create(
                    module=module_map[key].lower(), permission=data
                )
        self.stdout.write(self.style.SUCCESS("Permissions Configured Successfully"))
        return
