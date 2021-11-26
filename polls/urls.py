from rest_framework import routers
from polls.views import QuestionViewSet

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)


urlpatterns = router.urls
