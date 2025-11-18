---
description: 구현 계획에서 실행 가능한 작업 분석을 생성합니다.
---

## 사용자 입력

```text
$ARGUMENTS

```text
진행하기 전에 사용자 입력을 **반드시** 고려해야 합니다(비어있지 않은 경우).

## 개요

이 명령은 기능 사양과 구현 계획을 읽고 `/spec-mix.implement`가 실행할 수 있는 상세한 작업 분석을 생성합니다.

## 실행 흐름

1. **전제조건 확인**:
   - `spec.md`가 존재하고 완료됨
   - `plan.md`가 존재하고 완료됨
   - `research.md` 및 `data-model.md`가 존재함
   - **헌장**: `specs/constitution.md`가 존재하는 경우 작업 우선순위 및 구성을 위한 프로젝트 원칙 이해를 위해 로드

2. **사용자 스토리별 작업 생성**:
   - 각 사용자 스토리를 독립적인 구현 단계로 처리
   - 종속성 순서 존중 (예: 모델 → 서비스 → 엔드포인트)
   - 헌장이 존재하는 경우: 작업 분류 시 원칙 고려 (예: 테스트 요구사항, 코드 품질 표준, 관찰 가능성 요구사항)
   - 병렬 실행 가능한 작업 표시

3. **작업 분석 출력**:
   - 각 작업에 대한 명확한 설명
   - 구현할 정확한 파일 경로
   - 작업 간 종속성
   - 테스트 요구사항

4. **tasks.md에 쓰기**:
   - 템플릿 구조 사용
   - 각 사용자 스토리를 섹션으로
   - 체크포인트 검증 포함

5. **필수: 레인 구조와 함께 Work Package 파일 생성**:
   - **필수**: tasks.md 생성 후, 반드시 Work Package 디렉토리 구조 생성
   - **강제**: `FEATURE_DIR/tasks/`에 모든 하위 디렉토리 생성: `planned/`, `doing/`, `for_review/`, `done/`
   - tasks.md의 각 작업에 대해 `planned/`에 Work Package 파일 생성:
     - 파일명: `WPxx.y.md` (xx = 페이즈 번호, y = 페이즈 내 작업 번호)
     - `.spec-mix/active-mission/templates/work-package-template.md`를 템플릿으로 사용
     - frontmatter 필드 채우기:
       - `id`: WPxx.y (예: WP01.1, WP02.3)
       - `task_id`: tasks.md의 원래 작업 ID (예: T001)
       - `title`: 작업 설명에서 추출
       - `phase`: tasks.md의 페이즈 이름
       - `lane`: 처음에는 항상 "planned"
       - `status`: 처음에는 항상 "pending"
       - `created_at`: 현재 날짜 (YYYY-MM-DD)
       - `estimated_time`: 사용자가 채우도록 [ESTIMATED_TIME]으로 남겨둠
       - `depends_on`: Dependencies 섹션에서 파싱
     - tasks.md의 작업 세부사항으로 콘텐츠 섹션 채우기
   - **강제**: 워크플로우 적용을 위한 필수 레인 구조 생성:
     ```
     tasks/
     ├─ planned/     # 모든 작업이 여기서 시작
     │   ├─ WP01.1.md
     │   ├─ WP01.2.md
     │   └─ ...
     ├─ doing/       # 작업 시작 시 여기로 이동
     ├─ for_review/  # 구현 후 여기로 이동
     └─ done/        # 수락 후 여기로 이동
     ```
   - **워크플로우 규칙**: 작업은 반드시 이 순서를 따라야 함: planned → doing → for_review → done
   - **단축 금지**: 레인 건너뛰기나 역방향 이동 불가

6. **필수 워크플로우 안내**:
   사용자에게 다음 안내 표시:
   ```
   ⚠️ 레인 워크플로우가 이제 강제됩니다 ⚠️

   모든 작업이 'planned' 레인에 생성되었습니다.

   각 작업에 대한 필수 워크플로우:
   1. 선택: 작업할 항목 선택
   2. 이동: bash .spec-mix/scripts/move-task.sh WP## planned doing [FEATURE_DIR]
   3. 구현: 코드 작성 (커밋에 반드시 [WP##] 포함)
   4. 완료: bash .spec-mix/scripts/move-task.sh WP## doing for_review [FEATURE_DIR]
   5. 검토: /spec-mix.review 실행
   6. 수락: /spec-mix.accept 실행 (done으로 이동)

   ❌ /spec-mix.implement 명령이 차단되는 경우:
   - 'doing' 레인에 작업 없음
   - 커밋에 [WP##] 참조 누락
   - 완료된 작업이 리뷰로 이동되지 않음

   작업 레인 시각화: /spec-mix.dashboard 사용
   ```

## 작업 품질 기준

- 각 작업은 30분 이내에 완료 가능해야 함

- 작업은 명확하고 실행 가능해야 함

- 모든 파일 경로는 절대 경로여야 함

- 종속성이 명확하게 표시되어야 함
