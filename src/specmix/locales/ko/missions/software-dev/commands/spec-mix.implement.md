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

## 개요

1. 저장소 루트에서 `{SCRIPT}`를 실행하고 FEATURE_DIR 및 AVAILABLE_DOCS 목록을 파싱합니다. 모든 경로는 절대 경로여야 합니다. 'I'm Groot'와 같이 단일 따옴표가 포함된 인수의 경우 이스케이프 구문을 사용하세요: 예: 'I'\''m Groot' (또는 가능하면 큰따옴표: "I'm Groot").

2. **체크리스트 상태 확인** (FEATURE_DIR/checklists/가 존재하는 경우):
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

6. 작업 계획에 따라 구현 실행:
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

9. 완료 검증:
   - 필요한 모든 작업이 완료되었는지 확인
   - 구현된 기능이 원래 사양과 일치하는지 확인
   - 테스트가 통과하고 커버리지가 요구사항을 충족하는지 확인
   - 구현이 기술 계획을 따르는지 확인
   - 완료된 작업의 요약과 함께 최종 상태 보고

참고: 이 명령은 tasks.md에 완전한 작업 분석이 존재한다고 가정합니다. 작업이 불완전하거나 누락된 경우 먼저 `/spec-mix.tasks`를 실행하여 작업 목록을 재생성할 것을 제안합니다.

