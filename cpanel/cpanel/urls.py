"""cpanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index, name="index"),
    url(r'^about/',views.about, name="about"),
    url(r'^blog/',views.blog, name="blog"),
    url(r'^blog_single/',views.blog_single, name="blog_single"),
    url(r'^contact/',views.contact, name="contact"),
    url(r'^postcontact/',views.postcontact, name="postcontact"),
    url(r'^portfolio/',views.portfolio, name="portfolio"),
    url(r'^services/',views.services, name="services"),
    url(r'^team/',views.team, name="team"),
    url(r'^vendor_partner/',views.vendor_partner, name="vendor_partner"),
    url(r'^postvendor/',views.postvendor, name="postvendor"),
    url(r'^postdesign/',views.postdesign, name="postdesign"),
    url(r'^design_partner/',views.design_partner, name="design_partner"),
    url(r'^signIn/',views.signIn, name="signIn"),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^signUp/',views.signUp, name="signUp"),
    url(r'^postsignUp',views.postsignUp, name="postsignUp"),
    url(r'^prisoners/',views.Prisoners,name="prisoners"),
    url(r'^addPrisoner/',views.addPrisoner,name="add"),
    url(r'^viewprisoner/',views.viewPrisoner,name="viewp"),
    url(r'^postaddprisoner/',views.postaddprisoner,name="postadd"),
    url(r'^post_check/',views.post_check,name="pos_check"),
    url(r'addGuard/',views.addGuard,name="addg"),
    url(r'viewGuard/',views.viewGuards,name="viewg"),
    url(r'guards/',views.Guards,name="guards"),
    url(r'post_check2/',views.post_check2,name="post_check2"),
    url(r'postaddguard/',views.postaddguard,name="postaddg"),
    url(r'postaddvisitor/',views.postaddvisitor,name="postaddv"),
    url(r'viewVisitors/',views.viewVisitors,name="visitors")
]
