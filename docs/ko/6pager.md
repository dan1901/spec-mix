# 6-Pager 전략 문서 가이드

제품 전략 미션은 Amazon 스타일의 6-Pager 전략 문서를 AI의 도움으로 작성할 수 있게 해줍니다. 자동 웹 리서치와 출처 인용 기능이 포함되어 있습니다.

## 6-Pager란?

6-Pager는 Amazon에서 대중화된 구조화된 전략 문서 형식입니다. 간결한 형식 안에서 포괄적인 분석을 요구함으로써 명확한 사고를 강제합니다. 우리의 구현은 제품 전략의 모든 측면을 다루는 14개 섹션을 포함합니다.

## 빠른 시작

```bash
# product-strategy 미션으로 프로젝트 초기화
spec-mix init my-product --mission product-strategy --ai claude

cd my-product

# 6-Pager 문서 작성
/spec-mix.specify 밀레니얼을 위한 AI 기반 가계부 앱
```

## 문서 구조

6-Pager 템플릿은 14개 섹션으로 구성됩니다:

| # | 섹션 | 목적 |
|---|------|------|
| 1 | 한 줄 요약 | 한 문장으로 정리하는 엘리베이터 피치 |
| 2 | 배경과 목적 | 왜 지금? 어떤 문제? |
| 3 | 목표 & KPI | 비전과 측정 가능한 목표 |
| 4 | 시장 크기 | TAM/SAM/SOM 분석 |
| 5 | 고객 이해 | 페르소나와 JTBD |
| 6 | 경쟁사 분석 | 경쟁사 매트릭스와 포지셔닝 |
| 7 | 해결책 & USP | 핵심 기능과 차별화 |
| 8 | User Stories | 에픽과 유저 스토리 |
| 9 | 비즈니스 모델 | 수익 모델과 Unit Economics |
| 10 | GTM 전략 | 런칭과 마케팅 계획 |
| 11 | 제품 원칙 | 의사결정 가이드라인 |
| 12 | 마일스톤 | 로드맵과 핵심 결과물 |
| 13 | 리스크 | 리스크 매트릭스와 대응 방안 |
| 14 | 오픈 이슈 | 결정 필요 사항 |

## 사용 가능한 명령어

### `/spec-mix.specify`

자동 웹 리서치와 함께 대화형으로 6-Pager 문서를 작성합니다.

**사용법:**

```bash
# 기본 사용
/spec-mix.specify

# 제품 설명과 함께
/spec-mix.specify 원격 팀을 위한 B2B 프로젝트 관리 SaaS
```

**워크플로:**

1. **정보 수집** - AI가 제품에 대해 질문
2. **웹 리서치** - 시장 데이터, 경쟁사, 트렌드 자동 검색
3. **문서 생성** - 출처가 인용된 6-Pager 생성
4. **갭 식별** - 검증 필요 항목 목록화

### `/spec-mix.analyze`

특정 영역에 대한 심층 분석을 수행합니다.

**사용법:**

```bash
# 전체 분석
/spec-mix.analyze

# 시장 분석만
/spec-mix.analyze market

# 경쟁사 분석만
/spec-mix.analyze competitor

# 고객 분석만
/spec-mix.analyze customer
```

**결과물:**

- `specs/strategy/market-research.md`
- `specs/strategy/competitor-analysis.md`
- `specs/strategy/customer-analysis.md`

### `/spec-mix.refine`

피드백을 바탕으로 문서를 개선합니다.

**사용법:**

```bash
# 전반적 개선
/spec-mix.refine

# 특정 업데이트
/spec-mix.refine Gartner 2024 리포트 기반으로 TAM을 $75B로 업데이트

# 피드백 반영
/spec-mix.refine CFO가 CAC 상세 분석 요청
```

### `/spec-mix.review`

이해관계자 리뷰를 준비합니다.

**사용법:**

```bash
# 자체 품질 검토
/spec-mix.review self

# 피어 리뷰 준비
/spec-mix.review peer

# 이해관계자 리뷰 준비
/spec-mix.review stakeholder
```

## 웹 리서치 기능

AI가 자동으로 웹을 검색하여 6-Pager에 필요한 데이터를 수집합니다.

### 검색 대상

| 카테고리 | 검색 예시 |
|----------|----------|
| 시장 데이터 | "[산업명] market size 2024", "TAM SAM SOM" |
| 경쟁사 | "[회사명] funding", "pricing plans", "G2 reviews" |
| 트렌드 | "[산업명] trends 2024", "customer behavior" |

### 우선 검색 소스

**시장 데이터:**

- Statista, Gartner, IDC
- Grand View Research, MarketsandMarkets
- 통계청, 한국산업기술평가관리원

**경쟁사 정보:**

- Crunchbase (펀딩, 회사 정보)
- G2, Capterra (리뷰, 평점)
- 공식 웹사이트 (가격, 기능)
- LinkedIn (회사 규모, 성장)

### 출처 신뢰도

모든 데이터에는 신뢰도 표시가 붙습니다:

| 표시 | 의미 | 예시 |
|------|------|------|
| 🟢 검증됨 | 공식적, 권위있는 출처 | 정부 통계, IR 자료, 학술 논문 |
| 🟡 참고 | 신뢰할 수 있지만 비공식 | 뉴스 기사, 업계 블로그, 애널리스트 의견 |
| 🔴 추정 | 계산 또는 가정 기반 | 자체 계산, 외삽 추정 |

### 출처 인용 형식

```markdown
| 데이터 | 값 | 출처 | 신뢰도 | 접근일 |
|--------|-----|------|--------|--------|
| 글로벌 SaaS 시장 | $197B | [Statista](https://...) | 🟢 검증됨 | 2024-01-15 |
| 경쟁사 A ARR | $10M | [Crunchbase](https://...) | 🟡 참고 | 2024-01-15 |
```

## 워크플로 예시

### 예시 1: 신규 제품 런칭

```bash
# 초기화
spec-mix init fintech-app --mission product-strategy

# 6-Pager 작성
/spec-mix.specify Z세대를 위한 AI 저축 추천 기능의 개인 금융 앱

# 심층 분석
/spec-mix.analyze market
/spec-mix.analyze competitor

# 결과 반영
/spec-mix.refine

# 이사회 발표 준비
/spec-mix.review stakeholder
```

### 예시 2: 기능 확장

```bash
# 새 기능 전략 수립
/spec-mix.specify 기존 투자 앱에 암호화폐 포트폴리오 추적 기능 추가

# 경쟁 환경 집중 분석
/spec-mix.analyze competitor

# 팀 피드백 반영
/spec-mix.refine 개발팀이 암호화폐 API 지연시간 500ms라고 함 - 리스크에 추가
```

### 예시 3: 시장 진출

```bash
# 새 시장 기회 분석
/spec-mix.specify 프로젝트 관리 SaaS를 일본 시장으로 확장

# 시장 심층 분석
/spec-mix.analyze market
/spec-mix.analyze customer

# 준비 상태 점검
/spec-mix.review self
```

## 모범 사례

### 좋은 6-Pager 작성하기

**해야 할 것:**

- 숫자와 예시로 구체적으로 작성
- 모든 데이터에 출처 인용
- 기술이 아닌 고객 가치에 집중
- 리스크를 정직하게 식별하고 대응
- 간결하지만 완전하게 유지

**하지 말아야 할 것:**

- 근거 없는 낙관적 예측
- 가정을 사실처럼 표현
- 경쟁사 과소평가
- 리스크 무시하거나 숨기기
- 기술 중심 서술

### 정보가 없을 때

데이터가 없는 경우:

1. `[TBD]` 또는 `[검증 필요]`로 표시
2. 오픈 이슈 섹션에 추가
3. 검증 방법 명시
4. 담당자와 기한 지정

```markdown
### 오픈 이슈

| ID | 이슈 | 검증 방법 | 담당자 | 기한 |
|----|------|-----------|--------|------|
| OI-001 | APAC 지역 정확한 TAM | 시장 조사 의뢰 | PM | 2024 Q1 |
```

### 리뷰 프로세스

1. **자체 검토** - 완성도와 일관성 확인
2. **피어 리뷰** - 동료로부터 피드백
3. **이해관계자 리뷰** - 의사결정자에게 발표
4. **반복** - 피드백 기반 개선

## 결과 파일

명령어 실행 후 생성되는 파일:

```text
specs/
└── strategy/
    ├── 6pager.md              # 메인 전략 문서
    ├── market-research.md     # 상세 시장 분석
    ├── competitor-analysis.md # 경쟁사 심층 분석
    └── customer-analysis.md   # 페르소나 및 JTBD 분석
```

## 효과적인 사용 팁

### 1. 컨텍스트 준비

시작 전에 준비할 것:

- 제품 비전과 목표
- 알고 있는 경쟁사
- 타겟 고객 설명
- 기존 리서치 자료

### 2. 프롬프트를 구체적으로

```bash
# ❌ 너무 모호함
/spec-mix.specify 모바일 앱

# ✅ 구체적
/spec-mix.specify 프리랜서 디자이너가 클라이언트 프로젝트, 인보이스, 계약을 관리할 수 있는 모바일 앱. 타겟: 연소득 5천만-1억5천만원의 미국 기반 프리랜서
```

### 3. 자주 반복

한 번에 완벽하게 하려고 하지 마세요:

1. 초안 작성
2. 분석 실행
3. 결과 기반 개선
4. 검토하고 반복

### 4. 핵심 가정 검증

AI가 문서를 생성한 후:

- 시장 규모 수치 확인
- 경쟁사 정보 교차 검증
- 가격 가정 검증
- 고객 페르소나 테스트

## 문제 해결

### 웹 검색이 안 될 때

- 인터넷 연결 확인
- 더 구체적인 검색어 시도
- `/spec-mix.analyze`로 집중 리서치

### 출처를 찾을 수 없을 때

- 산업이 너무 니치할 수 있음
- 더 넓은 검색어 시도
- `[TBD]`로 표시하고 수동 리서치 필요 기록

### 문서가 너무 길 때

- 핵심 섹션에 먼저 집중
- `/spec-mix.refine`으로 정리
- 상세 내용은 부록으로 이동

## 다음 단계

6-Pager 완성 후:

1. **리뷰 공유** - 이해관계자 피드백 받기
2. **액션 플랜 작성** - 작업으로 분해
3. **Software-Dev로 전환** - 소프트웨어 개발 시, 미션 전환:

   ```bash
   spec-mix mission switch software-dev
   /spec-mix.specify [6-pager의 user stories 기반]
   ```

## 관련 문서

- [미션 시스템 개요](missions.md)
- [다국어 지원](i18n.md)
- [빠른 시작 가이드](quickstart.md)
