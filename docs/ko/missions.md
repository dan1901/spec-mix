# 미션 시스템

미션 시스템은 다양한 유형의 프로젝트에 최적화된 도메인별 워크플로 템플릿과 명령을 제공합니다.

## 미션이란?

미션은 특정 도메인에 사양 주도 개발을 적용하는 사전 구성된 워크플로 템플릿입니다. 각 미션에는 다음이 포함됩니다:

- **사용자 정의 슬래시 명령** - 도메인에 맞춤화
- **문서 템플릿** - 사전 구조화된 사양 및 계획
- **워크플로 가이드라인** - 도메인에 대한 모범 사례
- **헌법 템플릿** - 도메인별 원칙

## 사용 가능한 미션

### 소프트웨어 개발

**적합한 경우:** 웹 앱, 모바일 앱, API, 라이브러리, CLI 도구, 서비스

**기능:**

- 기능 기반 사양 구조
- 기술 세부사항이 포함된 구현 계획
- 개발 워크플로를 위한 작업 분해
- 코드 리뷰 및 테스트 체크리스트
- 아키텍처 결정 템플릿

**템플릿:**

- `spec-template.md` - 기능 사양
- `plan-template.md` - 기술 구현 계획
- `tasks-template.md` - 개발 작업 목록
- `checklist-template.md` - 품질 보증 체크리스트

**사용 예시:**

```bash
spec-mix init my-web-app --mission software-dev

# 소프트웨어 개발 명령 사용
/spec-mix.specify OAuth를 사용한 사용자 인증 추가
/spec-mix.plan PostgreSQL과 JWT 토큰 사용
/spec-mix.tasks 백엔드와 프론트엔드 작업으로 분해
```

### 제품 전략

**적합한 경우:** 제품 기획, 6-Pager 문서, 시장 분석, 비즈니스 케이스

**기능:**

- Amazon 스타일 6-Pager 전략 문서
- 시장 규모 분석 (TAM/SAM/SOM)
- 고객 페르소나 개발
- 경쟁사 분석 프레임워크
- 비즈니스 모델 캔버스
- GTM 전략 기획

**템플릿:**

- `6pager-template.md` - 14개 섹션 전략 문서
- `constitution-template.md` - 제품 전략 원칙

**명령:**

- `/spec-mix.specify` - 대화형으로 6-Pager 작성
- `/spec-mix.analyze` - 시장/경쟁사/고객 심층 분석
- `/spec-mix.refine` - 피드백 기반 문서 개선
- `/spec-mix.review` - 이해관계자 리뷰 체크리스트

**사용 예시:**

```bash
spec-mix init my-product --mission product-strategy

# 제품 전략 명령 사용
/spec-mix.specify 밀레니얼을 위한 AI 기반 가계부 앱
/spec-mix.analyze market
/spec-mix.analyze competitor
/spec-mix.refine Gartner 리포트 기반으로 TAM을 $10B로 업데이트
/spec-mix.review stakeholder
```

### 연구

**적합한 경우:** 학술 연구, 데이터 분석, 실험, 연구, 논문

**기능:**

- 연구 질문 공식화
- 문헌 검토 구조
- 방법론 문서화
- 데이터 분석 워크플로
- 결과 및 결론 템플릿

**템플릿:**

- `research-question-template.md` - 연구 질문 공식화
- `analysis-template.md` - 데이터 분석 문서화
- `findings-template.md` - 결과 및 결론

**사용 예시:**

```bash
spec-mix init ml-explainability-study --mission research

# 연구 명령 사용
/spec-mix.specify 연구 질문: 어텐션 메커니즘이 모델 해석 가능성을 어떻게 개선하는가?
/spec-mix.plan 기준 모델을 사용한 통제 실험 설계
/spec-mix.tasks 데이터 수집 및 분석 파이프라인 설정
```

## 미션 구조

각 미션은 로케일 디렉토리에 구성됩니다:

```text
src/specmix/locales/
└── [language]/
    └── missions/
        └── [mission-name]/
            ├── commands/          # 슬래시 명령
            │   ├── constitution.md
            │   ├── specify.md
            │   ├── plan.md
            │   ├── tasks.md
            │   ├── implement.md
            │   ├── review.md
            │   ├── accept.md
            │   ├── merge.md
            │   ├── clarify.md
            │   ├── analyze.md
            │   ├── checklist.md
            │   └── dashboard.md
            ├── templates/         # 문서 템플릿
            │   ├── spec-template.md
            │   ├── plan-template.md
            │   ├── tasks-template.md
            │   └── ...
            └── constitution/      # 가이드라인
                └── constitution-template.md
```

## 미션 사용

### 초기화 시

새 프로젝트를 만들 때 미션을 지정하세요:

```bash
# 소프트웨어 개발 (기본값)
spec-mix init my-app

# 명시적으로 software-dev 지정
spec-mix init my-app --mission software-dev

# 연구 프로젝트
spec-mix init my-study --mission research

# 언어와 결합
spec-mix init my-korean-research --mission research --language ko
```

### 미션 전환

기존 프로젝트의 미션을 변경할 수 있습니다:

```bash
# 사용 가능한 미션 목록
spec-mix mission list

# 다른 미션으로 전환
spec-mix mission set research

# 현재 미션 확인
spec-mix mission current
```

**참고:** 미션을 전환하면 `.claude/commands/`(또는 에이전트의 디렉토리)의 명령 파일이 업데이트되지만 기존 사양은 수정되지 않습니다.

## 미션별 명령 차이

### 소프트웨어 개발 명령

기능 구축에 중점을 둔 명령:

- **`/spec-mix.specify`** - 구축할 기능 설명
- **`/spec-mix.plan`** - 기술 구현 계획 작성
- **`/spec-mix.tasks`** - 개발 작업으로 분해
- **`/spec-mix.implement`** - 구현 실행
- **`/spec-mix.review`** - 코드 리뷰 체크리스트
- **`/spec-mix.accept`** - 승인 기준 검증

### 제품 전략 명령

전략 기획에 중점을 둔 명령:

- **`/spec-mix.specify`** - 6-Pager 전략 문서 작성
- **`/spec-mix.analyze`** - 시장/경쟁사/고객 분석
- **`/spec-mix.refine`** - 피드백 반영 및 문서 업데이트
- **`/spec-mix.review`** - 이해관계자 리뷰 및 승인

### 연구 명령

연구 워크플로에 중점을 둔 명령:

- **`/spec-mix.specify`** - 연구 질문 공식화
- **`/spec-mix.plan`** - 방법론 설계
- **`/spec-mix.tasks`** - 연구 활동 계획
- **`/spec-mix.implement`** - 연구 계획 실행
- **`/spec-mix.review`** - 동료 검토 체크리스트
- **`/spec-mix.accept`** - 결과 검증

## 사용자 정의 미션 만들기

특수 워크플로를 위한 자체 미션을 만들 수 있습니다.

### 1단계: 미션 디렉토리 생성

```bash
# 영어용
mkdir -p src/specmix/locales/en/missions/my-mission/commands
mkdir -p src/specmix/locales/en/missions/my-mission/templates
mkdir -p src/specmix/locales/en/missions/my-mission/constitution
```

### 2단계: 기본 템플릿 복사

기존 미션을 템플릿으로 시작하세요:

```bash
# software-dev를 기본으로 복사
cp -r src/specmix/locales/en/missions/software-dev/* \
      src/specmix/locales/en/missions/my-mission/
```

### 3단계: 명령 사용자 정의

각 명령 파일을 도메인에 맞게 편집하세요:

```markdown
---
description: 사용자 정의 명령 설명
scripts:
  sh: scripts/bash/your-script.sh
  ps: scripts/powershell/your-script.ps1
---

## 명령 지침

도메인에 맞는 워크플로 사용자 정의...
```

### 4단계: 템플릿 업데이트

도메인별 섹션을 포함하도록 템플릿 수정:

- 관련 섹션 추가
- 관련 없는 섹션 제거
- 예제 및 가이드 업데이트
- 용어 조정

### 5단계: 미션 테스트

```bash
spec-mix mission list           # 미션이 표시되어야 함
spec-mix init test --mission my-mission
```

## 미션 모범 사례

### 미션 선택

**소프트웨어 개발을 사용하는 경우:**

- 애플리케이션, 서비스 또는 도구 구축
- 기능 기반 사양 필요
- 구현 세부사항에 집중
- 코드 품질 검사 필요

**제품 전략을 사용하는 경우:**

- 제품 기획 문서 작성
- 시장/경쟁사 분석 필요
- 비즈니스 케이스 개발
- 이해관계자 프레젠테이션 준비
- 6-Pager 전략 문서 작성

**연구를 사용하는 경우:**

- 연구 또는 실험 수행
- 연구 질문 중심 필요
- 방법론 및 결과 문서화
- 분석 및 결론에 집중

**사용자 정의 미션을 만드는 경우:**

- 특수 도메인 요구사항
- 고유한 워크플로 필요
- 팀별 프로세스
- 하이브리드 접근 방식 필요

### 프로젝트 구성

```bash
# 미션 유형별로 그룹화
projects/
├── software/
│   ├── web-app/
│   ├── mobile-app/
│   └── api-service/
└── research/
    ├── ml-study/
    ├── user-research/
    └── performance-analysis/
```

### 미션 전환 가이드라인

**전환하기 좋은 시기:**

- 프로젝트 범위가 크게 변경됨
- 프로토타입에서 프로덕션으로 이동
- 연구에서 구현으로 전환

**전환을 피해야 할 때:**

- 활발한 개발 중
- 기존 사양이 일관성을 잃게 됨
- 팀이 현재 워크플로에 익숙함

## 다국어 미션

미션은 지원되는 모든 언어와 함께 작동합니다:

```bash
# 한국어 소프트웨어 개발
spec-mix init 내-앱 --mission software-dev --language ko

# 한국어 연구
spec-mix init 내-연구 --mission research --language ko
```

각 언어는 다른 미션 구현을 가질 수 있습니다:

```text
locales/
├── en/missions/
│   ├── software-dev/
│   └── research/
└── ko/missions/
    ├── software-dev/  # 한국어 버전
    └── research/      # 한국어 버전
```

## 예제

### 소프트웨어 개발 워크플로

```bash
# 초기화
spec-mix init todo-app --mission software-dev

cd todo-app

# 기능 정의
/spec-mix.specify 카테고리가 있는 작업 관리 생성

# 구현 계획
/spec-mix.plan React 프론트엔드, Node.js 백엔드, PostgreSQL 사용

# 작업 분해
/spec-mix.tasks

# 구현
/spec-mix.implement

# 검토 및 승인
/spec-mix.review
/spec-mix.accept
```

### 제품 전략 워크플로

```bash
# 초기화
spec-mix init my-saas --mission product-strategy

cd my-saas

# 6-Pager 작성 (대화형 가이드)
/spec-mix.specify B2B 프로젝트 관리 SaaS

# 심층 분석
/spec-mix.analyze market       # TAM/SAM/SOM 분석
/spec-mix.analyze competitor   # 경쟁 환경 분석
/spec-mix.analyze customer     # 페르소나 개발

# 피드백 반영
/spec-mix.refine CFO가 Unit Economics 상세화 요청

# 이해관계자 리뷰
/spec-mix.review stakeholder
```

### 연구 워크플로

```bash
# 초기화
spec-mix init attention-study --mission research

cd attention-study

# 질문 공식화
/spec-mix.specify 연구 질문: 어텐션 시각화가 모델 신뢰를 개선하는가?

# 연구 설계
/spec-mix.plan 설문조사와 메트릭을 사용한 혼합 방법 연구

# 활동 계획
/spec-mix.tasks

# 연구 실행
/spec-mix.implement

# 결과 문서화
/spec-mix.review
/spec-mix.accept
```

## 문제 해결

### 미션을 찾을 수 없음

```bash
# 사용 가능한 미션 목록
spec-mix mission list

# 미션 파일이 존재하는지 확인
ls src/specmix/locales/en/missions/
```

### 명령이 업데이트되지 않음

```bash
# 미션이 설정되었는지 확인
spec-mix mission current

# 명령 강제 업데이트
spec-mix mission set [mission-name] --force
```

### 사용자 정의 미션이 표시되지 않음

1. 디렉토리 구조가 예상 형식과 일치하는지 확인
2. 명령 파일에 적절한 프론트매터가 있는지 확인
3. 미션 이름이 기존 미션과 충돌하지 않는지 확인
4. 명령을 다시 로드하려면 AI 에이전트 재시작

## 고급 주제

### 미션 상속

다른 미션을 확장하는 미션을 만들 수 있습니다:

```bash
# 기본 미션
missions/software-dev/

# 확장 미션
missions/mobile-dev/  # 모바일별 템플릿으로 software-dev 확장
```

### 미션 플러그인

향후 기능: 미션을 플러그인으로 설치:

```bash
# 향후 기능
spec-mix mission install game-dev
spec-mix mission install devops
```

## 다음 단계

- [향상된 기능 개요](features.md)
- [다국어 가이드](i18n.md)
- [빠른 시작](quickstart.md)
