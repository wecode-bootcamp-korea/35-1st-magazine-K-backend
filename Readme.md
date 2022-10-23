# 프로젝트 소개

* 프로젝트명: Magazine k
* 개발기간: 2022.07.18-2022.07.29
* 개발인원: Frontend 3, Backend 2 (Backend 담당)
* 기술스택: Python, Django, MySQL

여러가지 콘텐츠를 바탕으로한 잡지 커머스 사이트를 구현해보았습니다. 짧게 정해진 프로젝트 기한에 맞추기 위해 기존의 커머스 사이트 Magazine b(https://magazine-b.co.kr/) 사이트의 기획을 클론하였습니다. 짧은 기간안에 결과물을 만들기 위해 웹 서비스 작성시 대부분의 기반이 이미 만들어져있는 장고 프레임워크를 사용하였습니다. 

## 구현

* 회원가입 및 로그인 기능 구현
* 상품리스트 조회, 정렬, 필터, 검색 및 페이지네이션 구현
* 상품 상세페이지 및 리뷰 기능 구현
* 장바구니 및 상품 주문 기능 구현

### 데이터베이스 다이어그램
---
![diagram](./image/schema.png)

### 프로젝트 구현 상세 (Backend)
---
* 로그인 및 회원가입

    최초 로그인 후 JWT를 이용하여 토큰 기반 인증 방식을 채택하였습니다.

    로그인한 클라이언트의 정보를 JWT payload에 담아 전달하고 클라이언트가 다른 작업에 대한 요청을 할 때 토큰을 전달합니다.

    이번 프로젝트에서 비회원의 장바구니 사용 및 주문은 불가능하여 인증, 인가 과정이 필요한 로직에 대하여 로그인 데코레이터를 구현하여 토큰의 유저 정보를 확인하고 기능들을 사용할 수 잇도록 구현하였습니다.

* 상품 리스트 페이지 및 상세 페이지

    상품 상세페이지에 진입할 시 상품의 전체 리스트를 불러옵니다. 클라이언트 측에서 카테고리를 선택하면 해당 카테고리에 대한 상품이 필터링 되어 데이터가 전달됩니다.

    상품을 요청에 따라 가격순 또는 최신순으로 정렬하여 데이터를 전달할 수 있습니다. 그리고 상품 리스트의 한 페이지에서 보고 싶은 상품 개수를 요청할 경우 페이지 당 상품의 개수를 pagenation하여 전달합니다.

    상품 상세 페이지에서는 하나의 상품에 대해 더 자세한 정보를 제공합니다.

* 상품 검색 기능

    상품 검색의 경우 상품 리스트 페이지 로직을 재활용하였습니다. 검색 키워드에 대한 필터 옵션을 추가하여 상품 이름을 기준으로 키워드가 포함된 상품 데이터를 응답하도록 구현하였습니다.

* 장바구니 및 상품 주문 기능 구현

    상품 주문에 대한 CRUD를 구현하였습니다.

    클라이언트가 상품을 장바구니에 넣으면 주문 테이블과 주문 상품 테이블에 정보가 업테이트 됩니다. 기획상 장바구니 테이블을 따로 두지 않고, 주문 상태 테이블에 장바구니를 하나의 상태로 하여 참조하도록 구현하였습니다.

    상품 주문 결재는 포인트를 소모하여 주문하는 방식으로 구현하였습니다. 배송 상테의 테이블에 다양한 상태가 존재하지만 해당 기능들은 구현하지 못하여 주문과 동시에 배송완료 상태가 되도록 하였습니다.

## API 설계

* User

|   End point   	| HTTP Method 	| Description 	| Status 	|
|:-------------:	|:-----------:	|:-----------:	|:------:	|
|  /member/join 	|     POST    	|   회원가입  	|  Done  	|
| /member/login 	|     POST    	|    로그인   	|  Done  	|

* Product

|          End point         	| HTTP Method 	| Description 	| Status 	|
|:--------------------------:	|:-----------:	|:-----------:	|:------:	|
|          /products         	|     GET     	| 제품 리스트 조회 	|  Done  	|
| /products/int:product_id 	|     GET     	|  제품 상세 조회  	|  Done  	|

* Order

|         End point        	|     HTTP Method     	|             Description             	| Status 	|
|:------------------------:	|:-------------------:	|:-----------------------------------:	|:------:	|
|       /orders/cart       	|         GET         	|            장바구니 조회            	|  Done  	|
| /orders/<int:product_id> 	| POST, PATCH, DELETE 	| 장바구니 상품 추가, 수량 조정, 삭제 	|  Done  	|
| /orders | PATCH | 상품 구매 | Done |

* Review

|                    End point                   	| HTTP Method 	|     Description     	| Status 	|
|:----------------------------------------------:	|:-----------:	|:-------------------:	|:------:	|
|        /products/int:product_id/reviews        	|  GET, POST  	| 리뷰 생성, 불러오기 	|  Done  	|
| /products/int:product_id/reviews/int:review_id 	|    DELETE   	|      리뷰 삭제      	|  Done  	|