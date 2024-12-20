"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

"""gifts_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from rest_framework_swagger.views import get_swagger_view

from . import settings


schema_view = get_swagger_view(
    title='GIFTs API Documentation',
    url='/' if settings.env.DEV_ENV else '/gifts/api/'
)

# Base URL patterns common to all environments
urlpatterns = [
    url(r'^docs/', schema_view),
    path('', include('restui.urls')),  # Root URL is reserved for restui
    path('users/', include('users.urls')),
]

# Dev environment-specific patterns
if settings.env.DEV_ENV:
    urlpatterns += [
        path('admin/', admin.site.urls),  # Admin included only in dev
    ]