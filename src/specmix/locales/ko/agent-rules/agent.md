# agent.md

이 파일은 AI 코딩 어시스턴트가 이 저장소의 코드를 다룰 때 참고하는 가이드입니다.

## 프로젝트 구성

이 프로젝트는 spec-mix 툴킷을 사용한 사양 주도 개발(Spec-Driven Development, SDD)을 따릅니다.

## Walkthrough 메모리 로드

**필수**: 각 세션 시작 시 기존 walkthrough 문서를 반드시 확인하고 로드하여 컨텍스트를 유지하세요:

```bash
# walkthrough 문서 확인
find specs -name "walkthrough.md" -type f
```

### 로드 우선순위

1. **즉시 실행**: `specs/` 디렉토리에서 `walkthrough.md` 파일 검색
2. **컨텍스트 로드**: 모든 walkthrough 읽어 이전 작업 이해
3. **결정 연속성**: 이전 세션의 동일한 패턴과 결정사항 적용

### Walkthrough 정보

각 walkthrough는 중요한 세션 메모리를 포함:
- 구현 요약
- 수정된 파일과 설명
- 기술 결정사항과 근거
- 테스트 결과와 검증 상태
- 미해결 이슈와 향후 작업
- Git 커밋 히스토리

## 사양 주도 개발 워크플로우

모든 기능에 대해 이 구조화된 접근법을 따르세요:

1. **설정 단계**:
   - `/spec-mix.constitution` - 프로젝트 원칙 정의
   - `/spec-mix.specify` - 기능 명세 작성

2. **계획 단계**:
   - `/spec-mix.clarify` - 모호한 부분 해결
   - `/spec-mix.plan` - 기술 구현 계획
   - `/spec-mix.tasks` - 상세 작업 분해

3. **구현 단계**:
   - `/spec-mix.analyze` - 아티팩트 교차 확인
   - `/spec-mix.implement` - 작업 실행 (walkthrough 자동 생성)

4. **검토 단계**:
   - `/spec-mix.review` - 완료된 작업 검토
   - `/spec-mix.accept` - 승인 검증
   - `/spec-mix.merge` - 메인에 통합

## 필수 사례

### 세션 시작 프로토콜

1. 기존 walkthrough 검색: `ls specs/*/walkthrough.md`
2. 이전 결정사항 로드 및 검토
3. 작업 레인 상태 확인: `ls specs/*/tasks/*/`
4. 마지막 알려진 상태에서 계속

### 구현 중

- 작업 시작 전 `doing` 레인에 있어야 함
- 커밋에 Work Package ID 포함: `[WP01] 설명`
- 작업 레인 이동: planned → doing → for_review → done
- 구현 후 walkthrough 자동 생성

### 세션 연속성

- Walkthrough는 세션 간 컨텍스트 보존
- 기술 결정사항은 일관되어야 함
- 아키텍처 패턴은 유지되어야 함
- 테스트 전략은 계속되어야 함

## 프로젝트 구조

```
project/
├── specs/                      # 기능 명세
│   └── {feature}/
│       ├── spec.md            # 기능 명세서
│       ├── plan.md            # 기술 계획
│       ├── tasks.md           # 작업 분해
│       ├── walkthrough.md     # 자동 생성된 세션 기록
│       └── tasks/             # 작업 레인 관리
│           ├── planned/
│           ├── doing/
│           ├── for_review/
│           └── done/
├── .spec-mix/                 # 툴킷 파일
│   └── scripts/               # 자동화 스크립트
└── .github/                   # GitHub 전용 (Copilot)
    └── commands/              # 슬래시 명령어

```

## 명령어 참조

- 초기화: `specify init <project-name>`
- 환경 확인: `specify check`
- 언어 설정: `specify lang`
- 미션 관리: `specify mission`
- 웹 대시보드: `specify dashboard`

## 중요 알림

⚠️ 세션 시작 시 **항상** walkthrough 확인
⚠️ 레인 워크플로우 **절대** 건너뛰지 말 것
⚠️ 커밋에 Work Package ID **항상** 참조
⚠️ Walkthrough는 자동 생성됨 - 수동으로 생성하지 말 것

## 통합 참고사항

- 이 파일은 GitHub Copilot, Codex CLI 및 유사한 에이전트와 작동
- AI 어시스턴트에 따라 명령어가 약간 다를 수 있음
- 핵심 워크플로우는 모든 에이전트에서 일관됨