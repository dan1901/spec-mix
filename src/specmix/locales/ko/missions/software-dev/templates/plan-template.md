# 구현 계획: [기능]

**브랜치**: `[###-feature-name]` | **날짜**: [날짜] | **사양**: [링크]
**입력**: `/specs/[###-feature-name]/spec.md`의 기능 사양

**참고**: 이 템플릿은 `/spec-mix.plan` 명령에 의해 작성됩니다. 실행 워크플로는 `.spec-mix/templates/commands/plan.md`를 참조하세요.

## 요약

[기능 사양에서 추출: 연구에서 기본 요구사항 + 기술적 접근 방식]

## 기술 컨텍스트

<!--
  조치 필요: 이 섹션의 내용을 프로젝트의 기술 세부사항으로 교체하세요.
  여기의 구조는 반복 프로세스를 안내하기 위한 권고 능력으로 제시됩니다.
-->

**언어/버전**: [예: Python 3.11, Swift 5.9, Rust 1.75 또는 명확화 필요]
**주요 종속성**: [예: FastAPI, UIKit, LLVM 또는 명확화 필요]
**스토리지**: [해당되는 경우, 예: PostgreSQL, CoreData, 파일 또는 해당 없음]
**테스팅**: [예: pytest, XCTest, cargo test 또는 명확화 필요]
**대상 플랫폼**: [예: Linux 서버, iOS 15+, WASM 또는 명확화 필요]
**프로젝트 유형**: [single/web/mobile - 소스 구조 결정]
**성능 목표**: [도메인별, 예: 1000 req/s, 10k lines/sec, 60 fps 또는 명확화 필요]
**제약조건**: [도메인별, 예: <200ms p95, <100MB 메모리, 오프라인 가능 또는 명확화 필요]
**규모/범위**: [도메인별, 예: 10k 사용자, 1M LOC, 50 화면 또는 명확화 필요]

## 헌장 확인

*게이트: 0단계 연구 전에 통과해야 함. 1단계 설계 후 재확인.*

[헌장 파일을 기반으로 결정된 게이트]

## 프로젝트 구조

### 문서 (이 기능)

```text
specs/[###-feature]/
├── plan.md              # 이 파일 (/spec-mix.plan 명령 출력)

├── research.md          # 0단계 출력 (/spec-mix.plan 명령)

├── data-model.md        # 1단계 출력 (/spec-mix.plan 명령)

├── quickstart.md        # 1단계 출력 (/spec-mix.plan 명령)

├── contracts/           # 1단계 출력 (/spec-mix.plan 명령)

└── tasks.md             # 2단계 출력 (/spec-mix.tasks 명령 - /spec-mix.plan으로 생성되지 않음)

```text

### 소스 코드 (저장소 루트)

<!--
  조치 필요: 아래 플레이스홀더 트리를 이 기능의 구체적인 레이아웃으로 교체하세요.
  사용하지 않는 옵션을 삭제하고 선택한 구조를 실제 경로로 확장하세요 (예: apps/admin, packages/something).
  제공된 계획에는 옵션 레이블이 포함되어서는 안 됩니다.
-->

```text

# [사용하지 않는 경우 제거] 옵션 1: 단일 프로젝트 (기본값)

src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [사용하지 않는 경우 제거] 옵션 2: 웹 애플리케이션 ("frontend" + "backend" 감지 시)

backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [사용하지 않는 경우 제거] 옵션 3: 모바일 + API ("iOS/Android" 감지 시)

api/
└── [위의 backend와 동일]

ios/ 또는 android/
└── [플랫폼별 구조: 기능 모듈, UI 흐름, 플랫폼 테스트]

```text
**구조 결정**: [선택한 구조를 문서화하고 위에 캡처된 실제 디렉토리 참조]

## 복잡성 추적

> **헌장 확인에 정당화되어야 하는 위반이 있는 경우에만 작성**

| 위반 | 필요한 이유 | 더 간단한 대안이 거부된 이유 |
|------|-----------|---------------------------|
| [예: 4번째 프로젝트] | [현재 필요] | [3개 프로젝트로 불충분한 이유] |
| [예: 리포지토리 패턴] | [특정 문제] | [직접 DB 액세스로 불충분한 이유] |
