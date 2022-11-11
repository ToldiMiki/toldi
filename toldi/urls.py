from django.urls import path
from django.contrib import admin
from toldi import views
from toldi.models import LogMessage
from toldi.models import CNjoke

"""home_list_view = views.HomeListView.as_view(
    queryset=CNjoke.objects.all,  #.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="joke_list",
    template_name="toldi/home.html",
)"""

cnjoke_list_view = views.cnjokeListView.as_view(
    queryset=CNjoke.objects.all,  #.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="joke_list",
    template_name="toldi/cnjoke.html",
)

urlpatterns = [
   #path("", cnjoke_list_view, name="home"),
    path("", views.home, name="home"),
    path("toldi/<name>", views.toldi_there, name="toldi_there"),
    path("about/", views.about, name="about"),
    path("cnjoke/", views.cnjoke, name="cnjoke"), #cnjoke_list_view, name="cnjoke"),
    path("cnjok1/", cnjoke_list_view, name="cnjok1"),
    path("log/", views.log_message, name="log"),
    path("admin/", admin.site.urls),
]
