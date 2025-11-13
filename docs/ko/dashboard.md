# 웹 대시보드

Spec Mix 대시보드는 사양 주도 개발 워크플로를 관리하고 보기 위한 시각적 인터페이스를 제공합니다.

## 개요

대시보드는 프로젝트의 사양, 계획 및 작업을 아름답고 탐색하기 쉬운 인터페이스에 표시하는 경량 웹 서버입니다.

**주요 기능:**

- 📊 시각적 기능 개요
- 📝 마크다운 렌더링
- 🔍 빠른 탐색
- 🎨 구문 강조
- 📱 반응형 디자인
- 🔄 자동 새로고침 기능

## 빠른 시작

### 대시보드 시작

```bash
# 기본 (포트 8080)
spec-mix dashboard

# 사용자 정의 포트
spec-mix dashboard --port 3000

# 네트워크에서 접근 가능하게 만들기
spec-mix dashboard --host 0.0.0.0 --port 8080

# 브라우저 자동 열기
spec-mix dashboard --browser
```

### 대시보드 접근

시작하면 브라우저에서 다음 주소를 여세요:

```text
http://localhost:8080
```

또는 사용자 정의 포트를 사용하는 경우:

```text
http://localhost:3000
```

### 대시보드 중지

터미널에서 `Ctrl+C`를 누르거나 다음을 사용하세요:

```bash
spec-mix dashboard --shutdown
```

## 대시보드 뷰

### 기능 목록

메인 뷰는 `specs/` 디렉토리의 모든 기능을 표시합니다:

```text
┌─────────────────────────────────────────────┐
│  Spec Mix Dashboard                         │
├─────────────────────────────────────────────┤
│                                             │
│  Features                                   │
│                                             │
│  ● 1-user-auth        [Specified]          │
│  ● 2-payment          [Planned]            │
│  ● 3-dashboard        [In Progress]        │
│  ○ 4-reports          [Not Started]        │
│                                             │
└─────────────────────────────────────────────┘
```

**표시되는 정보:**

- 기능 번호 및 이름
- 현재 상태
- 다음에 대한 빠른 링크:
  - 사양 (`spec.md`)
  - 계획 (`plan.md`)
  - 작업 (`tasks.md`)
  - 기타 문서

**상태 표시기:**

- 🟢 녹색 - 완료
- 🟡 노란색 - 진행 중
- 🔵 파란색 - 계획됨
- ⚪ 회색 - 시작하지 않음

### 문서 뷰어

전체 마크다운 렌더링으로 문서를 보려면 클릭하세요:

**기능:**

- 목차
- 구문 강조
- 코드 블록 포맷팅
- 링크 탐색
- 이미지 표시
- 테이블 렌더링

**키보드 단축키:**

- `←` - 기능 목록으로 돌아가기
- `Esc` - 문서 닫기

## 명령 옵션

### 기본 옵션

```bash
spec-mix dashboard [OPTIONS]
```

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--port` | 포트 번호 | 8080 |
| `--host` | 호스트 주소 | localhost |
| `--browser` | 브라우저 자동 열기 | false |
| `--shutdown` | 실행 중인 대시보드 중지 | - |

### 예제

```bash
# 포트 3000에서 실행
spec-mix dashboard --port 3000

# 팀(네트워크)에서 접근 가능하게 만들기
spec-mix dashboard --host 0.0.0.0

# 브라우저에서 자동 열기
spec-mix dashboard --browser

# 자동 열기와 함께 사용자 정의 포트
spec-mix dashboard --port 5000 --browser
```

## 사용 사례

### 개발 중

작업하는 동안 대시보드를 실행 상태로 유지:

```bash
# 터미널 1: 대시보드
spec-mix dashboard

# 터미널 2: 개발
cd specs/5-new-feature
# 사양 작업...

# http://localhost:8080에서 브라우저로 업데이트 보기
```

### 팀 데모

대시보드를 보여주는 화면 공유:

1. 대시보드 시작: `spec-mix dashboard --browser`
2. 기능 개요로 이동
3. 사양을 클릭하여 보기
4. 진행 상황 및 상태 표시

### 상태 검토

스탠드업 또는 계획 중 사용:

```bash
# 대시보드 시작
spec-mix dashboard --browser

# 각 기능의 상태 검토
# 진행 중인 항목을 클릭하여 보기
# 차단 요소 식별
```

### 원격 접근

원격 팀과 대시보드 공유:

```bash
# 컴퓨터에서 (먼저 IP 확인)
spec-mix dashboard --host 0.0.0.0 --port 8080

# 팀 멤버는 다음을 통해 접근:
# http://YOUR_IP:8080
```

**보안 참고:** 신뢰할 수 있는 네트워크에서만 `--host 0.0.0.0`을 사용하세요.

## 대시보드 구조

### 프로젝트 요구사항

대시보드는 다음 구조를 예상합니다:

```text
your-project/
├── specs/
│   ├── 1-feature-one/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── 2-feature-two/
│       ├── spec.md
│       └── plan.md
└── .spec-mix/
    └── memory/
        └── constitution.md
```

### 상태 감지

상태는 `spec.md`에서 추출됩니다:

```markdown
**Status**: In Progress
```

인식되는 상태:

- `Not Started` (시작하지 않음)
- `Specified` (사양 작성됨)
- `Planned` (계획됨)
- `In Progress` (진행 중)
- `In Review` (검토 중)
- `Completed` (완료)
- `Blocked` (차단됨)
- `On Hold` (보류)

### 문서 발견

대시보드는 자동으로 다음을 찾습니다:

- `specs/`의 모든 디렉토리
- 각 기능의 모든 `.md` 파일
- `.spec-mix/memory/`의 헌법

## 기술 세부사항

### 아키텍처

- **백엔드:** Python `http.server`
- **프론트엔드:** 바닐라 JavaScript
- **마크다운:** marked.js 라이브러리
- **강조:** highlight.js
- **스타일링:** 사용자 정의 CSS

### 파일 위치

```text
src/specmix/
├── dashboard.py              # 서버 로직
├── dashboard_command.py      # CLI 명령
└── static/
    └── dashboard/
        ├── index.html        # 메인 페이지
        ├── app.js           # 프론트엔드 로직
        └── styles.css       # 스타일링
```

### API 엔드포인트

대시보드는 간단한 API를 제공합니다:

```text
GET /                          # 메인 페이지
GET /api/features             # 모든 기능 목록
GET /api/feature/{name}       # 기능 세부정보 가져오기
GET /api/document/{feature}/{file}  # 문서 내용 가져오기
GET /api/shutdown             # 서버 중지
```

### 데이터 흐름

```text
브라우저 → JavaScript → API 엔드포인트 → Python → 파일 시스템
                     ←              ←        ←
```

## 사용자 정의

### 스타일링

`src/specmix/static/dashboard/styles.css` 편집:

```css
/* 색상 구성표 변경 */
:root {
  --primary-color: #0066cc;
  --background: #ffffff;
  --text-color: #333333;
}
```

### 기능 추가

`src/specmix/static/dashboard/app.js` 편집:

```javascript
// 사용자 정의 기능 추가
async function loadCustomData() {
  // 코드 작성
}
```

### 사용자 정의 템플릿

사용자 정의 문서 템플릿 생성:

1. 미션 템플릿에 템플릿 추가
2. 대시보드가 자동으로 발견
3. 기능 문서 목록에 표시

## 문제 해결

### 대시보드가 시작되지 않음

```bash
# 포트가 사용 중인지 확인
lsof -i :8080

# 다른 포트 사용
spec-mix dashboard --port 8081
```

### 기능이 표시되지 않음

```bash
# specs 디렉토리가 존재하는지 확인
ls specs/

# 디렉토리 명명 확인 (숫자-이름 형식이어야 함)
ls specs/ | grep -E '^[0-9]+-'
```

### 문서가 렌더링되지 않음

1. 마크다운 파일이 존재하는지 확인
2. 파일 인코딩이 UTF-8인지 확인
3. 마크다운의 구문 오류 확인

### 다른 컴퓨터에서 접근할 수 없음

```bash
# 올바른 호스트를 사용하는지 확인
spec-mix dashboard --host 0.0.0.0

# 방화벽 설정 확인
# 네트워크 연결 확인
ping YOUR_IP
```

### 포트가 이미 사용 중

```bash
# 포트를 사용하는 프로세스 찾기
lsof -i :8080

# 프로세스를 종료하거나 다른 포트 사용
spec-mix dashboard --port 8081
```

## 고급 사용

### CI/CD와 통합

CI/CD를 위한 정적 HTML 생성:

```bash
# 향후 기능
spec-mix dashboard --export ./dashboard-static/
```

### 자동화된 테스트

```bash
# 대시보드가 올바르게 시작되는지 테스트
spec-mix dashboard --test

# API 엔드포인트 확인
curl http://localhost:8080/api/features
```

### 성능

대시보드는 다음에 최적화되어 있습니다:

- **프로젝트:** 최대 100개 기능
- **문서:** 각각 최대 1MB
- **동시 사용자:** 최대 10명

더 큰 프로젝트의 경우 다음을 고려하세요:

- 여러 프로젝트로 나누기
- 정적 사이트 생성 사용
- 캐싱 구현

## 보안 고려사항

### 로컬 개발

로컬 사용을 위한 안전한 기본값:

```bash
# 컴퓨터에서만 접근 가능
spec-mix dashboard  # localhost 사용
```

### 팀 공유

팀과 공유할 때:

```bash
# 신뢰할 수 있는 네트워크에서만
spec-mix dashboard --host 0.0.0.0
```

**하지 말아야 할 것:**

- 공용 인터넷에 노출
- 신뢰할 수 없는 네트워크에서 사용
- 민감한 사양을 공개적으로 공유

**해야 할 것:**

- 원격 접근에 VPN 사용
- 인증 구현 (향후 기능)
- 공유 전에 사양 검토

## 향후 기능

계획된 개선사항:

- 🔐 인증/권한 부여
- 📊 진행 차트 및 메트릭
- 🔍 전체 텍스트 검색
- 📤 PDF/HTML로 내보내기
- 🎨 테마 및 사용자 정의
- 🔄 실시간 파일 감시
- 💬 댓글 및 주석
- 📱 모바일 앱

## 모범 사례

### 개발 중

1. 백그라운드에서 대시보드 실행 유지
2. 문서 저장 후 새로고침
3. 빠른 참조용으로 사용
4. 페어 프로그래밍을 위해 URL 공유

### 검토용

1. 스프린트 검토에 사용
2. 기능을 시각적으로 살펴보기
3. 이해관계자에게 진행 상황 표시
4. 사양에 대한 피드백 받기

### 문서용

1. 살아있는 문서로 사용
2. 새 팀 멤버와 공유
3. 계획 중 참조
4. 완료된 기능 보관

## 다음 단계

- [향상된 기능 개요](features.md)
- [미션 시스템](missions.md)
- [빠른 시작](quickstart.md)
- [로컬 개발](local-development.md)
