from rest_framework import serializers
from django.db.models import Q

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateReq(serializers.Serializer):
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


class CategoryCreateReq(serializers.Serializer):
    name = serializers.CharField(max_length=20)


class CategoryRepo:
    def __init__(self) -> None:
        pass

    def create_category(self, name: str) -> dict:
        created = Category.objects.create(name=name)
        return CategorySerializer(created).data


class ProductRepo:
    def __init__(self) -> None:
        pass

    def get_product_list_with_filter(
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

        list = (
            Product.objects.filter(filter_options)
            .order_by(sort_options[sort_by])
            .select_related("productimage")[offset : offset + limmit]
        )

        return ProductSerializer(list, many=True).data

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
    ) -> bool:
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
            main_category=Category.objects.get(id=main_category),
            sub_category=Category.objects.get(id=sub_category),
        )
        return ProductSerializer(created).data
