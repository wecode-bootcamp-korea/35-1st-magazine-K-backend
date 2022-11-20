from rest_framework import serializers
from django.db.models import Q
from django.db import transaction

from .models import Category, Product, ProductImage


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
    상품 등록 및 수정 요청 직렬화
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
    카테고리 등록 요청 직렬화
    """

    name = serializers.CharField(max_length=20)


class CategoryRepo:
    def __init__(self) -> None:
        pass

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

    def get_product_detail(self, product_id: int) -> dict:
        product = Product.objects.get(id=product_id)
        return ProductSerializer(product).data

    def get_product_and_image_list_with_filter(
        self,
        category: int,
        sort_by: str,
        offset: int,
        limmit: int,
        keyword: str,
    ) -> dict:
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
            .order_by(sort_options[sort_by])[offset : offset + limmit]
        )

        return ProductListSerializer(product_list, many=True).data

    # TODO 상품 id가 존재하지 않는 것에 대한 요청 유효성 검증 필요
    def update_product_and_image(
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
        Product.objects.filter(id=product_id).update(
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
            main_category=Category.objects.get(id=main_category),
            sub_category=Category.objects.get(id=sub_category),
        )
        return True

    def delete_product_and_image(self, product_id: int):
        Product.objects.get(id=product_id).delete()
        return True


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
