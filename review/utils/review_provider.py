from core.exceptions import AlreadyExistError, NotAuthorizationError, NotPurchasedError
from ..serializers import ReviewRepo
from order.serializers import OrderItemRepo

review_repo = ReviewRepo()
order_item_repo = OrderItemRepo()


class ReviewService:
    def create_review(self, product_id: int, user_id: int, content: str, rating: float) -> bool:
        """
        1. 주문한 상품에 대해서만 리뷰가 가능하다.
        2. 주문한 하나의 상품에 하나의 리뷰만 등록 가능하다.
        """
        item = order_item_repo.get_ordered_item_or_none(user_id=user_id, product_id=product_id)
        if not item:
            raise NotPurchasedError

        review = review_repo.get_review_or_none(user_id=user_id, product_id=product_id)
        if review:
            raise AlreadyExistError

        review_repo.create_review(
            product_id=product_id,
            user_id=user_id,
            content=content,
            rating=rating,
        )
        return True

    def get_review_list(self, product_id: int):
        return review_repo.get_review_list(product_id=product_id)

    def update_review(self, user_id: int, review_id: int, content: str) -> bool:
        review = review_repo.get_review_by_id(review_id=review_id)
        if not review.user_id == user_id:
            raise NotAuthorizationError
        review_repo.update_review_content(review_id=review_id, content=content)
        return True

    def delete_review(self, user_id: int, review_id: int) -> bool:
        review = review_repo.get_review_by_id(review_id=review_id)
        if not review.user_id == user_id:
            raise NotAuthorizationError
        review_repo.delete_review(review_id=review_id)
        return True
