# Indroduction

전 세계의 균형 잡힌 브랜드를 한 호에 담아 매거진으로 만들어 소개하는 Magazine B 웹페이지를 2주간의 프로젝트 기간동안 구현해보기 위해 팀 명처럼 (k) 팀의 각오를 담아 구현해보려 노력했습니다.

## Development

* 개발기간   : 2022/07/18 ~ 2022/07/29
* 개발인원   : 5 명
* Frontend : 주원영(PM), 길현민, 노정은
* Backend  : 김동규, 황유정

## Skill

|                                                Language                                                	|                                                   Framework                                                  	|                                                Database                                                	|                                                     Environment                                                    	|                                                    API                                                   	|
|:------------------------------------------------------------------------------------------------------:	|:------------------------------------------------------------------------------------------------------------:	|:------------------------------------------------------------------------------------------------------:	|:------------------------------------------------------------------------------------------------------------------:	|:--------------------------------------------------------------------------------------------------------:	|
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 	| ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) 	| ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) 	| ![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white) 	| ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) 	|

## Database

![database](Screenshot%20from%202022-07-30%2013-31-31.png)

## Implement

### Product List (GET)

* query Parameter
* Q 객체 필터링 구현

### Product Detail (GET)

* path parameter & query parameter
* Q 객체 필터링 구현

### Cart (GET, POST, PATCH, DELETE)

* path parameter & query parameter
* 특정 참조 데이터에 적용할 고유 상수값을 Enum Class로 정의
* Transaction을 활용하여 예외상황 발생 시 Roll back 적용

### Order (PATCH)

* path parameter
* Transaction을 활용하여 예외상황 발생 시 Roll back 적용

### Review

* path parameter
* 특정 참조 데이터에 적용할 고유 상수값을 Enum Class로 정의
* 구매한 상품에 한해 상품 리뷰를 작성할 수 있도록 로직 작성

## API

### User

|   End point   	| HTTP Method 	| Description 	| Status 	|
|:-------------:	|:-----------:	|:-----------:	|:------:	|
|  /member/join 	|     POST    	|   회원가입  	|  Done  	|
| /member/login 	|     POST    	|    로그인   	|  Done  	|

### Product

|          End point         	| HTTP Method 	| Description 	| Status 	|
|:--------------------------:	|:-----------:	|:-----------:	|:------:	|
|          /products         	|     GET     	| 제품 리스트 조회 	|  Done  	|
| /products/int:product_id 	|     GET     	|  제품 상세 조회  	|  Done  	|

### Order

|         End point        	|     HTTP Method     	|             Description             	| Status 	|
|:------------------------:	|:-------------------:	|:-----------------------------------:	|:------:	|
|       /orders/cart       	|         GET         	|            장바구니 조회            	|  Done  	|
| /orders/<int:product_id> 	| POST, PATCH, DELETE 	| 장바구니 상품 추가, 수량 조정, 삭제 	|  Done  	|
| /orders | PATCH | 상품 구매 | Done |

### Review

|                    End point                   	| HTTP Method 	|     Description     	| Status 	|
|:----------------------------------------------:	|:-----------:	|:-------------------:	|:------:	|
|        /products/int:product_id/reviews        	|  GET, POST  	| 리뷰 생성, 불러오기 	|  Done  	|
| /products/int:product_id/reviews/int:review_id 	|    DELETE   	|      리뷰 삭제      	|  Done  	|