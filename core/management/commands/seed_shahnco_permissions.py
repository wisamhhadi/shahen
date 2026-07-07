from django.core.management.base import BaseCommand

from core.models import Permission, PermissionGroup, Admin


ACTIONS = {
    "list": "عرض",
    "create": "إضافة",
    "update": "تعديل",
    "delete": "حذف",
}

# model_name هنا مفتاح منطقي نستخدمه لاحقاً لفحص الصلاحيات.
# لا يحتاج أن يطابق اسم موديل Django 100%.
PERMISSION_ITEMS = [
    # الإدارة العامة
    ("permission_group", "الصلاحيات", ["list", "create", "update", "delete"]),
    ("code_request", "طلبات الأكواد", ["list", "create", "update", "delete"]),
    ("file_manager", "مدير الملفات", ["list", "create", "update", "delete"]),
    ("pay", "سحب وإيداع الرصيد", ["list", "create", "update", "delete"]),
    ("financial_report", "الكشوفات المالية", ["list"]),

    # المدراء
    ("admin", "الموظفين", ["list", "create", "update", "delete"]),
    ("delete_account_request", "طلبات حذف الحسابات", ["list", "update", "delete"]),
    ("specialty", "التخصصات", ["list", "create", "update", "delete"]),

    # السيارات والمركبات
    ("car_model", "موديلات السيارات", ["list", "create", "update", "delete"]),
    ("car_size_main", "أحجام شحن رئيسية", ["list", "create", "update", "delete"]),
    ("car_size_sub", "أحجام شحن فرعية", ["list", "create", "update", "delete"]),
    ("car", "المركبات", ["list", "create", "update", "delete"]),
    ("car_color", "ألوان المركبات", ["list", "create", "update", "delete"]),
    ("car_company", "الشركات المصنعة", ["list", "create", "update", "delete"]),
    ("trailer", "أنواع القاطرات", ["list", "create", "update", "delete"]),
    ("car_category", "الفئات", ["list", "create", "update", "delete"]),
    ("car_year", "سنوات الصنع", ["list", "create", "update", "delete"]),
    ("car_letter", "الحروف", ["list", "create", "update", "delete"]),
    ("goods_type", "أنواع الحمولة", ["list", "create", "update", "delete"]),
    ("activity_type", "أنواع النشاط", ["list", "create", "update", "delete"]),
    ("country", "الدول", ["list", "create", "update", "delete"]),
    ("province", "المحافظات", ["list", "create", "update", "delete"]),

    # السائقين والمندوبين
    ("delivery_company", "الناقلين", ["list", "create", "update", "delete"]),
    ("captain", "السائقين", ["list", "create", "update", "delete"]),
    ("order", "الشحنات", ["list", "create", "update", "delete"]),
    ("mandob", "المندوبين", ["list", "create", "update", "delete"]),

    # التجار والمستخدمين
    ("merchant", "التجار", ["list", "create", "update", "delete"]),
    ("user", "المستخدمين", ["list", "create", "update", "delete"]),

    # الحسابات
    ("pre_paid", "الاشتراكات", ["list", "create", "update", "delete"]),

    # الإعدادات العامة
    ("notification", "إشعار عام", ["list", "create", "update", "delete"]),
    ("language", "اللغات", ["list", "create", "update", "delete"]),
    ("info", "الإعدادات العامة", ["list", "update"]),
    ("banner", "البنرات", ["list", "create", "update", "delete"]),
    ("blog", "المدونة", ["list", "create", "update", "delete"]),
]


GROUPS = {
    "L1 - مدير عام - كل الصلاحيات": {
        "keys": "*",
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير الإدارة العليا": {
        "keys": [
            "permission_group",
            "code_request",
            "file_manager",
            "pay",
            "financial_report",
            "admin",
            "delete_account_request",
            "specialty",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير المركبات": {
        "keys": [
            "car_model",
            "car_size_main",
            "car_size_sub",
            "car",
            "car_color",
            "car_company",
            "trailer",
            "car_category",
            "car_year",
            "car_letter",
            "goods_type",
            "activity_type",
            "country",
            "province",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير العمليات": {
        "keys": [
            "delivery_company",
            "captain",
            "order",
            "mandob",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير المستخدمين": {
        "keys": [
            "merchant",
            "user",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير الحسابات": {
        "keys": [
            "pay",
            "pre_paid",
            "financial_report",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L2 - مدير الإعدادات العامة": {
        "keys": [
            "notification",
            "language",
            "info",
            "banner",
            "blog",
            "country",
            "province",
        ],
        "actions": ["list", "create", "update", "delete"],
    },
    "L3 - موظف عرض فقط": {
        "keys": "*",
        "actions": ["list"],
    },
    "L3 - موظف عمليات": {
        "keys": [
            "delivery_company",
            "captain",
            "order",
            "mandob",
        ],
        "actions": ["list", "create", "update"],
    },
}


class Command(BaseCommand):
    help = "Seed Shahnco hierarchical permissions using existing Permission and PermissionGroup models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--assign-superusers",
            action="store_true",
            help="Assign the full permissions group to Admin users with is_superuser=True.",
        )

    def handle(self, *args, **options):
        permission_map = {}
        created_count = 0
        updated_count = 0

        for model_key, label, actions in PERMISSION_ITEMS:
            for action in actions:
                name = f"{label} - {ACTIONS[action]}"

                permission = Permission.objects.filter(name=name).first()

                if permission is None:
                    permission = Permission(name=name)
                    created_count += 1
                else:
                    updated_count += 1

                permission.model_name = model_key
                permission.create = action == "create"
                permission.update = action == "update"
                permission.list = action == "list"
                permission.delete = action == "delete"
                permission.is_active = True
                permission.save()

                permission_map[(model_key, action)] = permission

        all_keys = [item[0] for item in PERMISSION_ITEMS]

        for group_name, group_config in GROUPS.items():
            group, _ = PermissionGroup.objects.get_or_create(
                name=group_name,
                defaults={"is_active": True},
            )

            group.is_active = True
            group.save()

            keys = all_keys if group_config["keys"] == "*" else group_config["keys"]
            actions = group_config["actions"]

            group_permissions = []

            for key in keys:
                for action in actions:
                    permission = permission_map.get((key, action))
                    if permission is not None:
                        group_permissions.append(permission)

            group.permission.set(group_permissions)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Group ready: {group.name} | permissions={len(group_permissions)}"
                )
            )

        if options["assign_superusers"]:
            full_group = PermissionGroup.objects.get(name="L1 - مدير عام - كل الصلاحيات")
            qs = Admin.objects.filter(is_superuser=True)

            for admin in qs:
                admin.permission_group = full_group
                admin.save(update_fields=["permission_group"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned full permissions to superuser: {admin}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Created permissions: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"Updated permissions: {updated_count}"))
        self.stdout.write(self.style.SUCCESS("Shahnco permissions seed completed."))
