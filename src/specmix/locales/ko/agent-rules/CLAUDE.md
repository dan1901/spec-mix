# CLAUDE.md

이 파일은 Claude Code(claude.ai/code)가 이 저장소의 코드를 다룰 때 참고하는 가이드입니다.

## 프로젝트 구성

이 프로젝트는 spec-mix 툴킷을 사용한 사양 주도 개발(Spec-Driven Development, SDD)을 따릅니다.

## Walkthrough 메모리 로드

**중요**: 새 세션을 시작할 때 기존 walkthrough 문서를 확인하고 로드하세요:

```bash
# 현재 기능의 walkthrough 존재 여부 확인
if [ -f "specs/*/walkthrough.md" ]; then
    echo "이전 구현 컨텍스트 로드 중..."
fi
```

### Walkthrough 우선순위

1. **시작 시 첫 작업**: `specs/*/walkthrough.md` 파일 찾기
2. **컨텍스트 로드**: 구현 결정사항과 완료된 작업 기억하기
3. **참고 자료로 활용**: 작업 계속 시 이전 아키텍처 결정사항과 패턴 고려

### Walkthrough 구조

Walkthrough에 포함된 내용:
- 완료된 작업 요약
- 수정된 파일과 근거
- 아키텍처 결정사항
- 테스트 상태
- 알려진 이슈와 TODO
- 커밋 히스토리

## SDD 워크플로우

프로젝트는 다음의 구조화된 워크플로우를 따릅니다:

1. `/spec-mix.constitution` - 프로젝트 원칙 수립 (선택사항이지만 권장)
2. `/spec-mix.specify` - 기능 명세 작성
3. `/spec-mix.clarify` - 모호한 부분 명확화 (선택사항)
4. `/spec-mix.plan` - 기술 계획 작성
5. `/spec-mix.tasks` - 작업 분해 생성
6. `/spec-mix.analyze` - 교차 분석 (선택사항)
7. `/spec-mix.implement` - 구현 실행 (walkthrough 자동 생성)
8. `/spec-mix.review` - 완료된 작업 검토
9. `/spec-mix.accept` - 최종 승인 확인
10. `/spec-mix.merge` - 메인 브랜치에 병합

## 주요 명령어

- `specify init` - 프로젝트에 SDD 초기화
- `specify check` - 환경 검증
- `specify lang` - 언어 설정 관리
- `specify mission` - 개발 미션 전환
- `specify dashboard` - 웹 대시보드 실행

## 작업 세션 모범 사례

1. **세션 시작**: 기존 walkthrough 확인
2. **구현 중**: 레인 워크플로우 따르기 (planned → doing → for_review → done)
3. **세션 종료**: `/spec-mix.implement`에 의해 walkthrough 자동 생성
4. **컨텍스트 보존**: Walkthrough는 AI 상호작용 간 세션 메모리 역할

## 파일 위치

- 명세서: `specs/{feature-number}-{feature-name}/`
- Walkthrough: `specs/{feature}/walkthrough.md`
- 작업: `specs/{feature}/tasks/{lane}/*.md`
- 스크립트: `.spec-mix/scripts/`
- 명령어: `.claude/commands/`

## 중요 사항

- 작업 시작 전 항상 기존 walkthrough 확인
- 커밋 메시지에 Work Package ID 포함: `[WP01]`
- 레인 워크플로우 엄격히 준수
- Walkthrough는 자동 생성됨 - 수동으로 생성하지 말 것