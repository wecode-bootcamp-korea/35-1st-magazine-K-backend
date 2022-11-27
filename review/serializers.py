from rest_framework import serializers

from .models import Review
from core.exceptions import NotFoundReviewError


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewReq(serializers.Serializer):
    content = serializers.CharField()
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)


class ReviewUpdateReq(serializers.Serializer):
    content = serializers.CharField()


class ReviewRepo:
    def create_review(self, product_id: int, user_id: int, content: str, rating: float) -> dict:
        review = Review.objects.create(
            product_id=product_id,
            user_id=user_id,
            content=content,
            rating=rating,
        )
        return ReviewSerializer(review).data

    def get_review_or_none(self, user_id: int, product_id: int) -> object:
        review = Review.objects.filter(user_id=user_id, product_id=product_id)
        return review.first()

    def get_review_list(self, product_id: int) -> dict:
        reviews = Review.objects.filter(product_id=product_id)
        return ReviewSerializer(reviews, many=True).data

    def get_review_by_id(self, review_id: int) -> object:
        try:
            review = Review.objects.get(id=review_id)
            return review
        except Review.DoesNotExist:
            raise NotFoundReviewError

    def update_review_content(self, review_id: int, content: str) -> bool:
        Review.objects.filter(id=review_id).update(content=content)
        return True

    def delete_review(self, review_id: int) -> bool:
        Review.objects.get(id=review_id).delete()
        return True
