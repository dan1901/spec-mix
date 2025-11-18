---
id: [WP_ID]
task_id: [TASK_ID]
title: [TITLE]
phase: [PHASE]
lane: planned
status: pending
created_at: [DATE]
started_at: null
completed_at: null
estimated_time: [ESTIMATED_TIME]
actual_time: null
depends_on: [DEPENDENCIES]
files_modified: []
---

# [WP_ID]: [TITLE]

## 작업 목표

[OBJECTIVE]

## 파일 경로

[FILE_PATHS]

## 작업 내용

[WORK_CONTENT]

## 검증 기준

[ACCEPTANCE_CRITERIA]

## 종속성

[DEPENDENCIES_DETAIL]

## 병렬 실행

[PARALLEL_EXECUTION]

## 단위 테스트

[UNIT_TESTS]

## Git 히스토리

**커밋**: 커밋 메시지에 작업 ID가 포함되면 자동 추적 (다양한 형식 지원):
- `[WP_ID] 설명` (대괄호 형식)
- `feat: WP_ID 설명` (conventional commits)
- `WP_ID: 설명` (일반 형식)

**수정된 파일**: frontmatter의 `files_modified` 필드에 기록

<!--
이 섹션은 move-task.sh가 git commit을 감지할 때 자동으로 채워집니다.
형식: - [TIMESTAMP]: [GIT] [커밋해시] - [커밋메시지]
-->

## 활동 로그

**형식**:
- `[TIMESTAMP]: [ACTION]` - Lane 전환, 상태 변경
- `[TIMESTAMP]: [GIT] [hash] - [message]` - Git 커밋
- `[TIMESTAMP]: [NOTE] [description]` - 수동 메모
- `[TIMESTAMP]: [REVIEW] [decision] by [reviewer]` - 리뷰 결과

**로그**:
- [DATE]: 작업 생성됨
