from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# إذا عندك imports قديمة للصفحات، اتركها كما هي
# مثال:
# from home import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # API للموبايل
    path("api/", include("api.urls")),

    # روابط مشروعك القديمة اتركها هنا
    # مثال:
    # path("", views.home, name="home"),
    # path("profile", views.profile, name="profile"),
    # path("mandob_map", views.mandob_map, name="mandob_map"),
]

# ملفات media أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)