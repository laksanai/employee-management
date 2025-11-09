from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PositionViewSet, DepartmentViewSet, StatusViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'statuses', StatusViewSet)

urlpatterns = router.urls
