from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("products", views.ProductViewSet, basename='products')
router.register("catagorys", views.CatagoryViewSet, basename='catagorys')
router.register("customers", views.CustomerViewSet, basename='customers')
router.register("carts", views.CartViewSet, basename='carts')

products_router = routers.NestedDefaultRouter(router, "products", lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_item = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + cart_item.urls + products_router.urls