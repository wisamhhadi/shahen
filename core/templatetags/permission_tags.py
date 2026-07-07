from django import template

register = template.Library()


def user_has_permission(user, model_name, action):
    """
    فحص صلاحية مستخدم.
    مثال:
    model_name = "admin"
    action = "list"
    """
    try:
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        permission_group = getattr(user, "permission_group", None)

        if not permission_group or not permission_group.is_active:
            return False

        filters = {
            "model_name": model_name,
            "is_active": True,
            action: True,
        }

        return permission_group.permission.filter(**filters).exists()

    except Exception:
        return False


@register.filter
def has_perm_key(user, key):
    """
    الاستخدام داخل templates:
    {% if request.user|has_perm_key:"admin:list" %}
    """
    try:
        model_name, action = key.split(":")
        return user_has_permission(user, model_name, action)
    except Exception:
        return False