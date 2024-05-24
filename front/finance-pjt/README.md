# finance-pjt

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
### 5월 16일 목요일
- 컴포넌트 구성 및 Figma를 이용한 디자인 초안 작성
- 특이사항
  - 컴포넌트 구성 중 적금과 예금을 같은 컴포넌트에서 처리할 지 다른 컴포넌트에서 처리할 지 고민
  - 같은 페이지에서 처리 시 재사용성을 높일 수 있지만, 해당 컴포넌트가 받아야 하는 인자가 많아지고 더 컴포넌트 내부가 복잡해 질 것으로 보임(if의 사용이 늘어난다거나..)
  - 구현하면서 정하기로 결정

### 5월 17일 금요일
- 컴포넌트 구성에 맞춰 Vue skeleton 컴포넌트 제작
- 디자인 초안에 맞춰 App.vue의 navbar, 예적금 리스트업 페이지 작성
- 특이사항
  - 어떤 데이터를 받아올 것이냐, 그에 따라서 페이지를 어떻게 구성할 것인지 구상하는 것이 중요하고, 디자인 초안이 그런 부분이 부족함을 느낌(예를 들면 예적금 리스트업에서 은행 이미지를 가져온다거나)
  - 이런 부분은 백엔드와 계속 소통하면서 해결해야 할 듯(미리 다 정하는 게 가장 좋은 방향인 듯함)
  - 같은 맥락에서 기획, 디자인이 굉장히 중요함

### 5월 18일 토요일
- 디자인 초안에 맞춰 은행 기능(DepositView, SavingsView)의 detail 페이지와 예적금 리스트업 페이지 완성

### 5월 19일 일요일
- 로그인 페이지, 가까운 은행 찾기 디자인 초안 작성
- 디자인 초안에 맞춰 게시판 리스트업 페이지와 로그인 / 회원가입 페이지 완성

### 5월 20일 월요일
- axios를 통해 backend와 예적금 리스트업, 인증(로그인), 게시판 기능 연결
- 게시판 CRUD 기능 완성
- 특이사항
  - axios를 통해 데이터를 주고받으면서 디자인을 처음 만들 땐 생각하지 못했던 필요한 부분이나 필요없는 부분들이 많아 수정이 많이 필요했음
  - ERD를 더 신경쓰면서 디자인을 만들어야 함을 느낌

### 5월 21일 화요일
- 게시판 댓글 CRUD 기능 완성
- 가까운 은행 찾기 기능 완성

### 5월 22일 수요일
- axios를 통해 예적금 리스트업 완성(params를 보내고 backend는 그에 맞는 리스트 반환)
- 환율 계산기 디자인 작성 및 기능 완성
- 특이사항
  - SavingsView 안의 SavingsList 에서도 SavingsView의 함수를 사용할 일이 생기면서, pinia만으로 모든 것을 해결하기는 어렵다는 것을 느낌
  - props를 수업에서는 거의 Object에만 사용했는데, function을 주고받으면서 활용도가 많음을 느낌

### 5월 23일 목요일
- GPT 상품 추천 
- GPT에 금융상품 DB를 학습시켜 Backend DB와 연계한 상품 추천을 할 수 있도록 함

# front 사용방법
1. VSCode 실행 후 프로젝트 기본 위치에서 finance-pjt 폴더로 이동 
```$ cd front/finance-pjt/```
2. (Vue, Node.js 필요) 요구사항 설치 후 실행
```$ npm install```
```$ npm run dev```
3. URL http://localhost:5173/ 에 프론트엔드 서버가 실행됨

# 컴포넌트 구성
<pre>
App.vue
|
|ㅡDepositView
|   |ㅡㅡㅡㅡㅡㅡㅡ|
|   DepositQuiz  DepositList   
|   |            |
|   QuizCard     DepositDetail
|
|ㅡSavingsView
|   |ㅡㅡㅡㅡㅡㅡㅡ|
|   SavingsQuiz  SavingsList   
|   |            |
|   QuizCard     SavingDetail
|
|ㅡArticleView
|   |ㅡㅡㅡㅡㅡㅡㅡ|ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ|
|   ArticleList  ArticleCreateView        ArticleUpdateView
|   |             
|   ArticleDetail
|
|ㅡHomeView
|ㅡExchangeView
|ㅡFindBankView
|ㅡArticleView
|ㅡSigninView
|ㅡLoginView
</pre>
