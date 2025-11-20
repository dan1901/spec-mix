---
description: tasks.md에 정의된 모든 작업을 처리하고 실행하여 구현 계획을 실행합니다.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## 사용자 입력

```text
$ARGUMENTS

```text
진행하기 전에 사용자 입력을 **반드시** 고려해야 합니다(비어있지 않은 경우).

## 필수 레인 워크플로우 적용

**중요**: 다음 레인 워크플로우 규칙이 **엄격히 적용됩니다**:

1. **코드 작성 전**: 반드시 `doing` 레인에 작업이 있어야 함
2. **모든 커밋**: 반드시 작업 패키지 ID [WP##] 참조 필요
3. **완료 후**: 작업을 반드시 `for_review` 레인으로 이동

## 개요

1. 저장소 루트에서 `{SCRIPT}`를 실행하고 FEATURE_DIR 및 AVAILABLE_DOCS 목록을 파싱합니다. 모든 경로는 절대 경로여야 합니다. 'I'm Groot'와 같이 단일 따옴표가 포함된 인수의 경우 이스케이프 구문을 사용하세요: 예: 'I'\''m Groot' (또는 가능하면 큰따옴표: "I'm Groot").

2. **필수: 레인 상태 검증 및 작업 선택**:

   a. **현재 레인 상태 확인**:
      ```bash
      # 작업 디렉토리 존재 확인
      if [ ! -d "FEATURE_DIR/tasks" ]; then
          echo "오류: 작업 디렉토리를 찾을 수 없음. 먼저 /spec-mix.tasks 실행 필요"
          exit 1
      fi

      # 각 레인의 작업 수 확인
      PLANNED_COUNT=$(find FEATURE_DIR/tasks/planned -name "WP*.md" 2>/dev/null | wc -l)
      DOING_COUNT=$(find FEATURE_DIR/tasks/doing -name "WP*.md" 2>/dev/null | wc -l)
      REVIEW_COUNT=$(find FEATURE_DIR/tasks/for_review -name "WP*.md" 2>/dev/null | wc -l)
      DONE_COUNT=$(find FEATURE_DIR/tasks/done -name "WP*.md" 2>/dev/null | wc -l)
      ```

   b. **레인 상태 표시**:
      ```
      작업 레인 현황:
      ├─ planned:     [X개 작업]
      ├─ doing:       [X개 작업]
      ├─ for_review:  [X개 작업]
      └─ done:        [X개 작업]
      ```

   c. **강제: 작업할 항목 선택**:
      - DOING_COUNT > 0인 경우:
        - 현재 doing에 있는 작업 목록 표시
        - 질문: "기존 작업을 계속하시겠습니까, 새 작업을 선택하시겠습니까?"
      - DOING_COUNT = 0인 경우:
        - planned 레인의 모든 작업 나열
        - **필수** 사용자가 작업 선택: "어떤 작업을 진행하시겠습니까? (WP##)"
        - 선택하지 않으면 **차단**

   d. **선택한 작업을 doing으로 이동**:
      ```bash
      bash .spec-mix/scripts/move-task.sh WP## planned doing FEATURE_DIR
      ```
      - 활동 로그에 작업 이동 기록
      - 표시: "✓ WP##이 'doing' 레인으로 이동 - 작업 시작 가능"

3. **체크리스트 상태 확인** (FEATURE_DIR/checklists/가 존재하는 경우):
   - checklists/ 디렉토리의 모든 체크리스트 파일 스캔
   - 각 체크리스트에 대해 다음을 계산:
     - 전체 항목: `- [ ]` 또는 `- [X]` 또는 `- [x]`와 일치하는 모든 줄
     - 완료된 항목: `- [X]` 또는 `- [x]`와 일치하는 줄
     - 미완료 항목: `- [ ]`와 일치하는 줄
   - 상태 테이블 생성:

     ```text
     | 체크리스트 | 전체 | 완료 | 미완료 | 상태 |
     |-----------|------|------|--------|------|
     | ux.md     | 12   | 12   | 0      | ✓ 통과 |
     | test.md   | 8    | 5    | 3      | ✗ 실패 |
     | security.md | 6  | 6    | 0      | ✓ 통과 |
     ```

   - 전체 상태 계산:
     - **통과**: 모든 체크리스트의 미완료 항목이 0개
     - **실패**: 하나 이상의 체크리스트에 미완료 항목이 있음

   - **체크리스트가 미완료인 경우**:
     - 미완료 항목 수가 표시된 테이블 표시
     - **중지**하고 질문: "일부 체크리스트가 미완료입니다. 그래도 구현을 진행하시겠습니까? (yes/no)"
     - 계속하기 전에 사용자 응답 대기
     - 사용자가 "no" 또는 "wait" 또는 "stop"이라고 말하면 실행 중지
     - 사용자가 "yes" 또는 "proceed" 또는 "continue"라고 말하면 3단계로 진행

   - **모든 체크리스트가 완료된 경우**:
     - 모든 체크리스트가 통과했음을 보여주는 테이블 표시
     - 자동으로 3단계로 진행

3. 구현 컨텍스트 로드 및 분석:
   - **필수**: 전체 작업 목록 및 실행 계획을 위해 tasks.md 읽기
   - **필수**: 기술 스택, 아키텍처 및 파일 구조를 위해 plan.md 읽기
   - **헌장**: `specs/constitution.md`가 존재하는 경우 구현이 프로젝트 원칙을 따르도록 읽기 (코드 품질, 테스트 표준, 아키텍처 제약조건)
   - **존재하는 경우**: 엔티티 및 관계를 위해 data-model.md 읽기
   - **존재하는 경우**: API 사양 및 테스트 요구사항을 위해 contracts/ 읽기
   - **존재하는 경우**: 기술적 결정 및 제약 조건을 위해 research.md 읽기
   - **존재하는 경우**: 통합 시나리오를 위해 quickstart.md 읽기

4. **프로젝트 설정 확인**:
   - **필수**: 실제 프로젝트 설정을 기반으로 무시 파일 생성/확인:

   **감지 및 생성 로직**:
   - 다음 명령이 성공하는지 확인하여 저장소가 git 저장소인지 확인 (그런 경우 .gitignore 생성/확인):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Dockerfile* 존재 또는 plan.md에 Docker가 있는지 확인 → .dockerignore 생성/확인
   - .eslintrc* 또는 eslint.config.* 존재 확인 → .eslintignore 생성/확인
   - .prettierrc* 존재 확인 → .prettierignore 생성/확인
   - .npmrc 또는 package.json 존재 확인 → .npmignore 생성/확인 (게시하는 경우)
   - terraform 파일 (*.tf) 존재 확인 → .terraformignore 생성/확인
   - .helmignore 필요 확인 (helm 차트가 있는 경우) → .helmignore 생성/확인

   **무시 파일이 이미 존재하는 경우**: 필수 패턴이 포함되어 있는지 확인하고 누락된 중요 패턴만 추가
   **무시 파일이 없는 경우**: 감지된 기술에 대한 전체 패턴 세트로 생성

   **기술별 공통 패턴** (plan.md 기술 스택에서):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **범용**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **도구별 패턴**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. tasks.md 구조를 파싱하고 추출:
   - **작업 단계**: Setup, Tests, Core, Integration, Polish
   - **작업 종속성**: 순차 실행 vs 병렬 실행 규칙
   - **작업 세부정보**: ID, 설명, 파일 경로, 병렬 마커 [P]
   - **실행 흐름**: 순서 및 종속성 요구사항

6. **필수 워크플로우: 엄격한 레인 적용으로 구현 실행**:

   **코드 작성 전**:
   - **정지**: 선택한 작업(2단계에서)이 `doing` 레인에 있는지 확인
   - **차단**: doing에 작업이 없으면 표시:
     ```
     ❌ 오류: 'doing' 레인에 작업 없음
     코드 작성 전에 반드시 작업을 'doing'으로 이동해야 합니다.
     실행: bash .spec-mix/scripts/move-task.sh WP## planned doing FEATURE_DIR
     ```
   - **진행**: 작업이 `doing` 레인에 있을 때만 진행

   **구현 중**:
   - **단계별 실행**: 다음 단계로 이동하기 전에 각 단계를 완료
   - **종속성 존중**: 순차 작업을 순서대로 실행, 병렬 작업 [P]는 함께 실행 가능
   - **TDD 접근 방식 따르기**: 해당 구현 작업 전에 테스트 작업 실행
   - **파일 기반 조정**: 동일한 파일에 영향을 미치는 작업은 순차적으로 실행해야 함
   - **검증 체크포인트**: 진행하기 전에 각 단계 완료를 확인

7. 구현 실행 규칙:
   - **설정 먼저**: 프로젝트 구조, 종속성, 구성 초기화
   - **코드보다 테스트**: 계약, 엔티티 및 통합 시나리오에 대한 테스트를 작성해야 하는 경우
   - **핵심 개발**: 모델, 서비스, CLI 명령, 엔드포인트 구현
   - **통합 작업**: 데이터베이스 연결, 미들웨어, 로깅, 외부 서비스
   - **마무리 및 검증**: 단위 테스트, 성능 최적화, 문서화

8. 진행 상황 추적 및 오류 처리:
   - 완료된 각 작업 후 진행 상황 보고
   - 순차 작업이 실패하면 실행 중지
   - 병렬 작업 [P]의 경우 성공한 작업을 계속하고 실패한 작업을 보고
   - 디버깅을 위한 컨텍스트가 포함된 명확한 오류 메시지 제공
   - 구현을 진행할 수 없는 경우 다음 단계 제안
   - **중요: 작업 상태 관리 (하이브리드 접근 방식)**:

     **자동 감지**: 시스템이 프로젝트 구조를 기반으로 적절한 방법을 자동으로 선택합니다:

     **옵션 1 - Work Package 파일 시스템 (가장 권장, move-task.sh 사용)**:
     - **감지**: `FEATURE_DIR/tasks/` 디렉토리에 `planned/`, `doing/`, `for_review/`, `done/` 서브디렉토리와 WPxx.md 파일이 있는 경우
     - **사용 방법**:
       1. **작업 시작 전**:
          ```bash
          bash scripts/bash/move-task.sh WP01 planned doing "$FEATURE_DIR"
          ```
       2. **작업 완료 후** (검토 필요):
          ```bash
          bash scripts/bash/move-task.sh WP01 doing for_review "$FEATURE_DIR"
          ```
       3. **검토 완료 후**:
          ```bash
          bash scripts/bash/move-task.sh WP01 for_review done "$FEATURE_DIR"
          ```
     - **장점**:
       - Work Package 파일의 frontmatter (lane, started_at, completed_at) 자동 업데이트
       - 활동 로그 자동 추가
       - 대시보드와 완벽하게 통합
       - 각 작업이 독립된 파일로 관리되어 병합 충돌 감소
     - **참고**: FEATURE_DIR은 check-prerequisites.sh의 출력에서 가져옵니다

     **옵션 2 - tasks.md 섹션 기반 (Work Package 파일이 없는 경우)**:
     - **감지**: tasks.md에 상태 섹션 (## Planned, ## Doing, ## For Review, ## Done)이 포함된 경우
     - **사용 방법**:
       1. **작업 시작 전**: `## Planned` 섹션에서 `## Doing` 섹션으로 작업 이동
       2. **작업 완료 후**: `## Doing` 섹션에서 `## Done` 섹션으로 작업 이동
       3. **작업에 검토가 필요한 경우**: `## Doing` 섹션에서 `## For Review` 섹션으로 작업 이동
     - 형식: 전체 작업 항목 (### WP-XXX: 제목 + 설명)을 잘라내어 대상 섹션에 붙여넣기
     - 이렇게 하면 대시보드 칸반 보드에서 작업 상태가 표시됩니다

     **옵션 3 - 체크박스 기반 (가장 간단, 섹션도 없는 경우)**:
     - **감지**: tasks.md가 섹션 없이 체크박스 형식만 사용하는 경우
     - **사용 방법**:
       1. **시작 전**: `- [ ] TXXX`를 `- [ ] TXXX (진행 중)`으로 변경
       2. **완료 후**: `- [ ] TXXX`를 `- [x] TXXX`로 변경

     **섹션 생성 (옵션 2를 사용하고 싶지만 섹션이 없는 경우)**:
     - tasks.md에 상태 섹션이 없지만 대시보드 지원을 원하는 경우 추가:
       ```markdown
       ## Planned
       [예정된 작업을 여기로 이동]

       ## Doing
       [현재 작업 중인 작업을 여기로 이동]

       ## For Review
       [검토 대기 중인 작업을 여기로 이동]

       ## Done
       [완료된 작업을 여기로 이동]
       ```
     - 그런 다음 모든 작업 헤더 (### WP-XXX 또는 ### TXXX)를 적절한 섹션으로 이동

   - **필수 Git 커밋 규칙**:

     **적용**: 모든 커밋은 이 규칙을 따라야 함 - 예외 없음:

     1. **커밋 전 - doing 상태 확인**:
        ```bash
        # 작업이 doing 레인에 있는지 확인
        ls FEATURE_DIR/tasks/doing/WP*.md
        # 비어있으면: 중지 - 먼저 작업을 doing으로 이동
        ```

     2. **커밋 메시지 형식 - 필수**:
        ```bash
        git commit -m "[WP##] 변경 사항 간단 설명

        - 상세 변경 사항 1
        - 상세 변경 사항 2

        작업: WP## - [작업 제목]
        레인: doing -> for_review (이 커밋 후)"
        ```

     3. **커밋 전 검증**:
        - **확인**: WP## 작업이 `doing/` 레인에 존재
        - **확인**: 커밋 메시지에 [WP##] 포함
        - **차단**: 하나라도 실패시:
          ```
          ❌ 커밋 차단: 요구사항 누락
          - 작업이 'doing' 레인에 있어야 함
          - 커밋 메시지에 [WP##] 포함 필요
          ```

     4. **커밋 후 - 자동으로 리뷰로 이동**:
        ```bash
        # 성공적인 커밋 후 즉시 작업 이동
        bash .spec-mix/scripts/move-task.sh WP## doing for_review FEATURE_DIR
        echo "✓ WP## 작업이 리뷰로 이동 - /spec-mix.review 실행 준비됨"
        ```

     **예시**:
     ```bash
     # 좋은 커밋 메시지 (대괄호 안에 작업 ID)
     git commit -m "[WP01.1] HttpMethod enum 모델 추가

     - src/models/enums.py에 HttpMethod 클래스 생성
     - GET, POST, PUT, DELETE, PATCH 메서드 추가
     - docstring 및 type hint 포함"

     git commit -m "[WP02.3] 사용자 인증 미들웨어 구현

     - JWT 토큰 검증 추가
     - src/middleware/auth.py에 인증 미들웨어 생성
     - 기존 사용자 모델과 통합"

     git commit -m "[T005] 로그인 검증 버그 수정

     - 이메일 검증 null pointer 수정
     - 잘못된 형식의 이메일에 대한 오류 처리 추가"
     ```

     **이것이 중요한 이유**:
     - `move-task.sh` 스크립트가 `[TASK_ID]` 패턴과 일치하는 커밋을 자동 감지
     - 커밋이 Work Package Activity Log에 자동 추가됨
     - 대시보드에서 작업별 git 히스토리 표시
     - 코드 변경의 자동 감사 추적 생성

     **자동으로 추적되는 항목**:
     - 커밋 해시, 메시지, 타임스탬프, 작성자
     - 각 커밋에서 수정된 파일 목록
     - 각 작업의 변경 타임라인

     **모범 사례**:
     - 빈번하고 작은 커밋 만들기 (리뷰 및 되돌리기 쉬움)
     - 항상 시작 부분에 작업 ID 포함: `[WP01]`, `[WP01.1]`, `[T005]`
     - 명확하고 설명적인 커밋 메시지 작성
     - 각 논리적 작업 단위 완료 후 커밋
     - 관련 변경 사항을 단일 커밋으로 그룹화

9. **필수 작업 완료 워크플로우**:

   **적용**: 작업 완료는 반드시 이 워크플로우를 따라야 함:

   a. **작업 완료 확인**:
      - [WP##] 참조와 함께 모든 코드 변경 커밋
      - 테스트 작성 및 통과
      - 문서 업데이트

   b. **필수: 작업을 리뷰로 이동**:
      ```bash
      # 완료된 작업을 반드시 리뷰로 이동
      bash .spec-mix/scripts/move-task.sh WP## doing for_review FEATURE_DIR
      ```
      - 작업 이동하지 않으면 추가 작업 **차단**
      - 표시: "✓ WP## 리뷰 준비 완료 - /spec-mix.review 사용"

   c. **완료 후 레인 상태**:
      ```
      최종 레인 상태:
      ├─ planned:     [남은 작업]
      ├─ doing:       [0이어야 함 - 모두 리뷰로 이동]
      ├─ for_review:  [리뷰 대기 중인 완료된 작업]
      └─ done:        [검토 및 승인된 작업]
      ```

   d. **다음 단계 안내**:
      ```
      ✓ WP##의 구현 단계 완료

      필수 다음 단계:
      1. /spec-mix.review 실행하여 완료된 작업 검토
      2. 검토 후 /spec-mix.accept 실행하여 수락
      3. 수락 후 작업이 'done'으로 이동

      ⚠️ 검토 완료 전까지 새 작업 시작 금지
      ```

10. **워크플로우 요약**:

    모든 작업에 대한 강제 워크플로우:
    ```
    planned → doing → for_review → done
      ↓         ↓         ↓          ↓
    선택      구현      검토      수락됨
    ```

    **단축 금지**:
    - 레인 건너뛰기 불가
    - doing에 작업 없이 커밋 불가
    - 완료된 작업을 doing에 남겨둘 수 없음
    - 완전한 워크플로우 준수 필수

참고: 이 명령은 완전한 레인 워크플로우를 강제합니다. 구현 전 작업이 반드시 'doing'에 있어야 하고, 완료 후 반드시 'for_review'로 이동해야 합니다.

## Walkthrough 생성 (자동)

구현 작업 완료 후, 작업 증명과 세션 메모리 역할을 하는 walkthrough 문서를 자동으로 생성합니다:

### Walkthrough 문서 생성

**위치**: `specs/{feature}/walkthrough.md`

다음 구조를 사용하여 포괄적인 walkthrough를 생성하세요:

```markdown
# 구현 Walkthrough: {feature}

**생성 시각**: {timestamp}
**세션 ID**: {unique-session-id}

## 요약

이 세션에서 구현한 내용의 간략한 개요.

## 완료된 작업

### 구현된 작업
- WP## - {작업 설명}: {상태}
- 이 세션에서 작업한 모든 작업 나열

### 수정된 파일
```
{git diff --name-status 출력}
```

### 주요 변경사항

#### {컴포넌트/모듈 이름}
- **파일**: {파일 경로}
- **변경사항**: {변경 설명}
- **근거**: {이 접근법을 선택한 이유}

{수정된 각 주요 컴포넌트에 대해 반복}

## 테스트 및 검증

### 실행한 테스트
```bash
{테스트 명령과 출력}
```

### 수동 검증
- [ ] 개발 환경에서 기능 테스트
- [ ] 엣지 케이스 처리
- [ ] 오류 시나리오 테스트

## 아키텍처 결정사항

중요한 기술적 결정사항 문서화:
- 특정 패턴을 선택한 이유
- 고려한 트레이드오프
- 거부한 대안과 그 이유

## 알려진 이슈 및 TODO

- [ ] 구현 중 발견된 남은 이슈
- [ ] 식별된 향후 개선사항
- [ ] 발생한 기술 부채

## 커밋 히스토리

```bash
git log --oneline --graph --decorate --since="{session-start}"
```

## 다음 단계

다음에 해야 할 작업:
1. for_review 레인의 작업 검토
2. 식별된 후속 작업
3. 필요한 문서 업데이트

---
*이 walkthrough는 이번 구현 세션 동안 완료된 작업과 내린 결정사항의 기록입니다.*
```

### 자동 저장 및 참조

Walkthrough 생성 후:
1. `specs/{feature}/walkthrough.md`에 저장
2. 메시지 표시: "✓ Walkthrough 생성됨: specs/{feature}/walkthrough.md"
3. 이 파일은 다음 세션에서 AI 에이전트가 자동으로 로드합니다 (에이전트 구성을 통해)

