from django.conf import settings
from django.conf.urls.static import static

app_name = "text_tonality_analyze"

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
