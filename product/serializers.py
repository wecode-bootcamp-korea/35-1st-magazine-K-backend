from rest_framework import serializers
from django.db.models import Q

from .models import Category, Product, ProductImage
from core.exceptions import NotFoundProductError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["main_url", "sub_url"]


class ProductListSerializer(serializers.ModelSerializer):
    productimage = ProductImageSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "price", "issue_number", "main_category", "productimage"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductReq(serializers.Serializer):
    """
    상품 등록, 수정 요청 직렬화 클래스
    """

    title = serializers.CharField(max_length=30)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    language = serializers.CharField(max_length=20)
    size = serializers.CharField(max_length=30)
    pages = serializers.IntegerField()
    published_date = serializers.CharField(max_length=20)
    isbn = serializers.CharField(max_length=20)
    description = serializers.CharField()
    issue_number = serializers.IntegerField()
    product_image_url = serializers.CharField(max_length=200)
    main_category = serializers.IntegerField()
    sub_category = serializers.IntegerField()
    main_url = serializers.CharField()
    sub_url = serializers.CharField()


class CategoryReq(serializers.Serializer):
    """
    카테고리 등록 요청 직렬화 클래스
    """

    name = serializers.CharField(max_length=20)


class CategoryRepo:
    def create_category(self, name: str) -> dict:
        created = Category.objects.create(name=name)
        return CategorySerializer(created).data

    def get_category(self, category_id: int) -> object:
        return Category.objects.get(id=category_id)

    def get_category_list(self) -> dict:
        categories = Category.objects.all()
        return CategorySerializer(categories, many=True).data

    def update_category(self, category_id: int, name: str) -> bool:
        Category.objects.filter(id=category_id).update(name=name)
        return True

    def delete_category(self, category_id: int) -> bool:
        Category.objects.get(id=category_id).delete()
        return True


class ProductRepo:
    def __init__(self) -> None:
        self.category_repo = CategoryRepo()

    def create_product(
        self,
        title: str,
        price: int,
        language: str,
        size: str,
        pages: int,
        published_date: str,
        isbn: str,
        description: str,
        issue_number: int,
        product_image_url: str,
        main_category: int,
        sub_category: int,
    ) -> object:
        created = Product.objects.create(
            title=title,
            price=price,
            language=language,
            size=size,
            pages=pages,
            published_date=published_date,
            isbn=isbn,
            description=description,
            issue_number=issue_number,
            product_image_url=product_image_url,
            main_category=self.category_repo.get_category(category_id=main_category),
            sub_category=self.category_repo.get_category(category_id=sub_category),
        )
        return ProductSerializer(created).data

    def get_product_with_title_and_isbn(self, title: str, isbn: int):
        return Product.objects.filter(title=title, isbn=isbn)

    def get_product(self, product_id: int) -> dict:
        try:
            product = Product.objects.get(id=product_id)
            return ProductSerializer(product).data
        except Product.DoesNotExist:
            raise NotFoundProductError

    def get_product_and_image_list_with_filter(
        self,
        category: int,
        sort_by: str,
        offset: int,
        limit: int,
        keyword: str,
    ) -> dict:
        """
        필터, 정렬 옵션을 적용하여 해당되는 상품의 목록을 응답합니다.

        "sort_options"는 (최신 순, 오래된 순), (높은 가격 순, 낮은 가격 순)으로 정렬 옵션을 제공합니다.
        "filter_options"는 특정 매개변수가 들어왔을 때 해당 필터를 적용하도록 하였습니다.
        이러한 두 가지 옵션을 적용하여 "product_image"테이블을 조인하여 데이터를 제공합니다.
        """
        sort_options = {
            "latest_issue": "-issue_number",
            "oldest_issue": "issue_number",
            "high_price": "-price",
            "low_price": "price",
        }

        filter_options = Q()

        if category:
            filter_options |= Q(main_category=category)
            filter_options |= Q(sub_category=category)

        if keyword:
            filter_options &= Q(title__icontains=keyword)

        product_list = (
            Product.objects.select_related("productimage")
            .filter(filter_options)
            .order_by(sort_options[sort_by])[offset : offset + limit]
        )

        return ProductListSerializer(product_list, many=True).data

    def update_product(
        self,
        product_id: int,
        title: str,
        price: int,
        language: str,
        size: str,
        pages: int,
        published_date: str,
        isbn: str,
        description: str,
        issue_number: int,
        product_image_url: str,
        main_category: int,
        sub_category: int,
    ) -> bool:
        product = Product.objects.filter(id=product_id)
        if not product:
            raise NotFoundProductError
        product.update(
            title=title,
            price=price,
            language=language,
            size=size,
            pages=pages,
            published_date=published_date,
            isbn=isbn,
            description=description,
            issue_number=issue_number,
            product_image_url=product_image_url,
            main_category=self.category_repo.get_category(category_id=main_category),
            sub_category=self.category_repo.get_category(category_id=sub_category),
        )
        return True

    def delete_product_and_image(self, product_id: int):
        try:
            Product.objects.get(id=product_id).delete()
            return True
        except Product.DoesNotExist:
            raise NotFoundProductError


class ProductImageRepo:
    def create_product_image(self, product_id: int, main_url: str, sub_url: str) -> dict:
        created = ProductImage.objects.create(
            product_id=product_id,
            main_url=main_url,
            sub_url=sub_url,
        )
        return ProductImageSerializer(created).data

    def update_product_image(self, product_id: int, main_url: str, sub_url: str) -> dict:
        ProductImage.objects.filter(product_id=product_id).update(
            main_url=main_url,
            sub_url=sub_url,
        )
        return True
