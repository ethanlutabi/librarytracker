from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, TagViewSet, BookViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('tags', TagViewSet)

urlpatterns = router.urls