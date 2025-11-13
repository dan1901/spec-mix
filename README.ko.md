<div align="center">
    <img src="./media/logo.png" alt="Spec Mix Logo" width="120"/>
    <h1>🌱 Spec Mix</h1>
    <h3><em>고품질 소프트웨어를 더 빠르게 구축하세요.</em></h3>
</div>

<p align="center">
    <strong>제품 시나리오와 예측 가능한 결과에 집중할 수 있도록 하는 오픈소스 툴킷입니다.</strong>
</p>

<p align="center">
    <a href="https://github.com/github/spec-kit/actions/workflows/release.yml"><img src="https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/github/spec-kit/stargazers"><img src="https://img.shields.io/github/stars/github/spec-kit?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/github/spec-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/github/spec-kit" alt="License"/></a>
    <a href="https://dan1901.github.io/spec-kit/"><img src="https://img.shields.io/badge/docs-GitHub_Pages-blue" alt="Documentation"/></a>
</p>

> **📢 Fork 공지**: 이 프로젝트는 [github/spec-kit](https://github.com/github/spec-kit)의 포크로, **다국어 지원(i18n)**이 추가되었습니다. 완전한 한국어 번역과 커뮤니티 번역을 위한 확장 가능한 아키텍처가 포함되어 있습니다. 자세한 내용은 [Fork 정보](#-fork-정보)를 참조하세요.

**Language / 언어**: [English](README.md) | **한국어**

---

## 목차

- [🤔 Spec-Driven Development란?](#-spec-driven-development란)

- [⚡ 시작하기](#-시작하기)

- [📽️ 비디오 개요](#️-비디오-개요)

- [🤖 지원되는 AI 에이전트](#-지원되는-ai-에이전트)

- [🌍 다국어 지원](#-다국어-지원)

- [🔧 Spec Mix CLI 참조](#-spec-mix-cli-참조)

- [📚 핵심 철학](#-핵심-철학)

- [🌟 개발 단계](#-개발-단계)

- [🎯 실험적 목표](#-실험적-목표)

- [🔧 전제 조건](#-전제-조건)

- [📖 더 알아보기](#-더-알아보기)

- [📋 상세 프로세스](#-상세-프로세스)

- [🔍 문제 해결](#-문제-해결)

- [👥 메인테이너](#-메인테이너)

- [💬 지원](#-지원)

- [🙏 감사의 말](#-감사의-말)

- [🔀 Fork 정보](#-fork-정보)

- [📄 라이선스](#-라이선스)

## 🤔 Spec-Driven Development란?

Spec-Driven Development는 전통적인 소프트웨어 개발의 **판도를 바꿉니다**. 수십 년 동안 코드가 왕이었고, 명세는 단지 "실제 작업"인 코딩을 시작하면 버려지는 비계에 불과했습니다. Spec-Driven Development는 이를 바꿉니다: **명세가 실행 가능해지고**, 단순히 안내하는 것이 아니라 직접 작동하는 구현을 생성합니다.

## ⚡ 시작하기

### 1. Spec Mix CLI 설치

선호하는 설치 방법을 선택하세요:

#### 옵션 1: 영구 설치 (권장)

한 번 설치하고 어디서나 사용:

```bash
uv tool install spec-mix --from git+https://github.com/dan1901/spec-mix.git

```

그런 다음 도구를 직접 사용:

```bash
spec-mix init <PROJECT_NAME>
spec-mix check

```

spec-mix를 업그레이드하려면:

```bash
uv tool install spec-mix --force --from git+https://github.com/dan1901/spec-mix.git

```

#### 옵션 2: 일회성 사용

설치 없이 직접 실행:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <PROJECT_NAME>

```

**영구 설치의 장점:**

- 도구가 설치되어 PATH에서 사용 가능

- 쉘 별칭 생성 불필요

- `uv tool list`, `uv tool upgrade`, `uv tool uninstall`로 더 나은 도구 관리

- 더 깔끔한 쉘 구성

### 2. 프로젝트 원칙 수립

프로젝트 디렉토리에서 AI 어시스턴트를 실행하세요. `/spec-mix.*` 명령어를 어시스턴트에서 사용할 수 있습니다.

**`/spec-mix.constitution`** 명령을 사용하여 모든 후속 개발을 안내할 프로젝트의 지배 원칙과 개발 가이드라인을 만드세요.

```bash
/spec-mix.constitution 코드 품질, 테스팅 표준, 사용자 경험 일관성, 성능 요구사항에 중점을 둔 원칙 생성

```

### 3. 명세 생성

**`/spec-mix.specify`** 명령을 사용하여 구축하려는 것을 설명하세요. 기술 스택이 아닌 **무엇을**과 **왜**에 집중하세요.

```bash
/spec-mix.specify 사진을 별도의 포토 앨범으로 정리할 수 있는 애플리케이션을 만들어주세요. 앨범은 날짜별로 그룹화되며 메인 페이지에서 드래그 앤 드롭으로 재정렬할 수 있습니다. 앨범은 다른 중첩 앨범 안에 있지 않습니다. 각 앨범 내에서 사진은 타일 형태의 인터페이스로 미리보기됩니다.

```

### 4. 기술 구현 계획 생성

**`/spec-mix.plan`** 명령을 사용하여 기술 스택과 아키텍처 선택을 제공하세요.

```bash
/spec-mix.plan 애플리케이션은 최소한의 라이브러리로 Vite를 사용합니다. 가능한 한 바닐라 HTML, CSS, JavaScript를 사용하세요. 이미지는 어디에도 업로드되지 않으며 메타데이터는 로컬 SQLite 데이터베이스에 저장됩니다.

```

### 5. 작업으로 분해

**`/spec-mix.tasks`**를 사용하여 구현 계획에서 실행 가능한 작업 목록을 생성하세요.

```bash
/spec-mix.tasks

```

### 6. 구현 실행

**`/spec-mix.implement`**를 사용하여 모든 작업을 실행하고 계획에 따라 기능을 구축하세요.

```bash
/spec-mix.implement

```

자세한 단계별 지침은 [종합 가이드](./spec-driven.md)를 참조하세요.

## 📽️ 비디오 개요

Spec Kit의 실제 동작을 보고 싶으신가요? [비디오 개요](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)를 시청하세요!

## 🤖 지원되는 AI 에이전트

| 에이전트                                                     | 지원 | 비고                                             |
|-----------------------------------------------------------|---------|---------------------------------------------------|
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli)             | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [Codex CLI](https://github.com/openai/codex)              | ✅ |                                                   |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI는 슬래시 명령에 대한 사용자 정의 인수를 [지원하지 않습니다](https://github.com/aws/amazon-q-developer-cli/issues/3064). |
| [Amp](https://ampcode.com/) | ✅ | |

## 🌍 다국어 지원

Spec Kit은 명령어, 템플릿 및 CLI 인터페이스에 대한 다국어를 지원하여 전 세계 개발자가 접근할 수 있습니다.

### 지원되는 언어

| 언어 | 코드 | 상태 | 커버리지 |
|----------|------|--------|----------|
| English  | `en` | ✅ 기본값 | 100% (CLI + 명령 + 템플릿) |
| 한국어   | `ko` | ✅ 사용 가능 | 100% (CLI + 명령 + 템플릿) |

### 선호하는 언어로 Spec Kit 사용

Spec Kit은 시스템 언어를 자동으로 감지합니다. 특정 언어를 사용하려면:

#### 빠른 시작

```bash
# 환경 변수로 언어 설정 (영구적)
export SPECIFY_LANG=ko

# 또는 세션별로 사용
SPECIFY_LANG=ko spec-mix init my-project

```

#### 언어 관리 명령

```bash
# 사용 가능한 언어 목록
spec-mix lang list

# 현재 언어 표시
spec-mix lang current

# 기본 언어 설정
spec-mix lang set ko

```

#### 미션 관리 명령

```bash
# 사용 가능한 미션 목록
spec-mix mission list

# 현재 미션 정보 표시
spec-mix mission current

# 미션 전환
spec-mix mission switch research

# 미션 세부정보 보기
spec-mix mission info software-dev

```

#### 대시보드 명령

```bash
# 대시보드 시작 (브라우저에서 열림)
spec-mix dashboard

# 특정 포트에서 시작
spec-mix dashboard start --port 9000

# 대시보드 상태 확인
spec-mix dashboard status

# 대시보드 중지
spec-mix dashboard stop

```

### 번역되는 내용

선호하는 언어로 Spec Kit을 사용할 때 다음이 번역됩니다:

- **CLI 메시지**: 모든 프롬프트, 오류, 성공 메시지 및 도움말 텍스트

- **명령 지침**: 모든 `/spec-mix.*` 슬래시 명령 워크플로우

  - `/spec-mix.specify`, `/spec-mix.plan`, `/spec-mix.tasks` 등

- **템플릿**: 명세, 구현 계획 및 작업 분해 템플릿

- **문서**: 생성된 파일 내의 인라인 주석 및 가이드

### 예제: 한국어 워크플로우

```bash
# 한국어 설정
export SPECIFY_LANG=ko

# 프로젝트 초기화 (모든 프롬프트가 한국어로)
spec-mix init my-project --ai claude

# 한국어로 슬래시 명령 사용
/spec-mix.constitution  # 프로젝트 원칙 수립
/spec-mix.specify       # 기능 사양 생성
/spec-mix.plan          # 구현 계획 생성
/spec-mix.tasks         # 작업 분석 생성
/spec-mix.implement     # 구현 실행

```

### 번역 기여

귀하의 언어에 대한 지원을 추가하고 싶으신가요? 커뮤니티 번역을 환영합니다! 다음에 대한 [국제화 가이드](docs/i18n.md)를 참조하세요:

- 새 언어 설정

- 번역 가이드라인 및 모범 사례

- 번역 테스트

- 기여 제출

자세한 문서는 **[docs/i18n.md](docs/i18n.md)**를 참조하세요.

## 🔧 Spec Mix CLI 참조

`specify` 명령은 다음 옵션을 지원합니다:

### 명령

| 명령     | 설명                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | 최신 템플릿에서 새 Spec Mix 프로젝트 초기화      |
| `check`     | 설치된 도구 확인 (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |
| `lang`      | 언어 팩 관리 (`list`, `current`, `set`, `install`)    |
| `mission`   | 미션 관리 (`list`, `current`, `switch`, `info`)    |
| `dashboard` | 웹 대시보드 관리 (`start`, `stop`, `status`)    |

### `spec-mix init` 인수 및 옵션

| 인수/옵션              | 유형     | 설명                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | 인수 | 새 프로젝트 디렉토리 이름 (`--here` 사용 시 선택 사항, 현재 디렉토리의 경우 `.` 사용) |
| `--ai`                 | 옵션   | 사용할 AI 어시스턴트: `claude`, `gemini`, `copilot`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, 또는 `q` |
| `--script`             | 옵션   | 사용할 스크립트 변형: `sh` (bash/zsh) 또는 `ps` (PowerShell)                 |
| `--lang`               | 옵션   | 사용할 언어: `en`, `ko` (기본값: `en`)                                 |
| `--mission`            | 옵션   | 사용할 미션: `software-dev`, `research` (기본값: `software-dev`)        |
| `--ignore-agent-tools` | 플래그     | Claude Code와 같은 AI 에이전트 도구 확인 건너뛰기                             |
| `--no-git`             | 플래그     | git 저장소 초기화 건너뛰기                                          |
| `--here`               | 플래그     | 새 디렉토리를 만드는 대신 현재 디렉토리에서 프로젝트 초기화   |
| `--force`              | 플래그     | 현재 디렉토리에서 초기화할 때 강제 병합/덮어쓰기 (확인 건너뛰기) |
| `--skip-tls`           | 플래그     | SSL/TLS 확인 건너뛰기 (권장하지 않음)                                 |
| `--debug`              | 플래그     | 문제 해결을 위한 자세한 디버그 출력 활성화                            |
| `--github-token`       | 옵션   | API 요청을 위한 GitHub 토큰 (또는 GH_TOKEN/GITHUB_TOKEN 환경 변수 설정)  |

### 예제

```bash
# 기본 프로젝트 초기화
spec-mix init my-project

# 특정 AI 어시스턴트로 초기화
spec-mix init my-project --ai claude

# Cursor 지원으로 초기화
spec-mix init my-project --ai cursor-agent

# Windsurf 지원으로 초기화
spec-mix init my-project --ai windsurf

# Amp 지원으로 초기화
spec-mix init my-project --ai amp

# 한국어로 초기화
spec-mix init my-project --ai claude --lang ko

# 연구 미션으로 초기화
spec-mix init my-project --ai claude --mission research

# 언어와 미션 모두 지정하여 초기화
spec-mix init my-project --ai claude --lang ko --mission research

# 대화형 선택 (지정하지 않으면 언어와 미션을 묻습니다)
spec-mix init my-project --ai claude

# PowerShell 스크립트로 초기화 (Windows/크로스 플랫폼)
spec-mix init my-project --ai copilot --script ps

# 현재 디렉토리에서 초기화
spec-mix init . --ai copilot
# 또는 --here 플래그 사용
spec-mix init --here --ai copilot

# 확인 없이 현재 (비어 있지 않은) 디렉토리로 강제 병합
spec-mix init . --force --ai copilot
# 또는
spec-mix init --here --force --ai copilot

# git 초기화 건너뛰기
spec-mix init my-project --ai gemini --no-git

# 문제 해결을 위한 디버그 출력 활성화
spec-mix init my-project --ai claude --debug

# API 요청을 위한 GitHub 토큰 사용 (기업 환경에 유용)
spec-mix init my-project --ai claude --github-token ghp_your_token_here

# 시스템 요구사항 확인
spec-mix check

```

### 사용 가능한 슬래시 명령

`spec-mix init`을 실행한 후 AI 코딩 에이전트는 구조화된 개발을 위해 다음 슬래시 명령에 액세스할 수 있습니다:

#### 핵심 명령

Spec-Driven Development 워크플로우를 위한 필수 명령:

| 명령                  | 설명                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/spec-mix.constitution`  | 프로젝트 지배 원칙 및 개발 가이드라인 생성 또는 업데이트 |
| `/spec-mix.specify`       | 구축하려는 것 정의 (요구사항 및 사용자 스토리)        |
| `/spec-mix.plan`          | 선택한 기술 스택으로 기술 구현 계획 생성     |
| `/spec-mix.tasks`         | 구현을 위한 실행 가능한 작업 목록 생성                     |
| `/spec-mix.implement`     | 계획에 따라 기능을 구축하기 위해 모든 작업 실행         |

#### 워크플로우 관리 명령

워크트리 및 작업 레인으로 기능 개발을 관리하는 명령:

| 명령              | 설명                                                           |
|----------------------|-----------------------------------------------------------------------|
| `/spec-mix.dashboard` | 웹 대시보드를 실행하여 기능, 칸반 보드 및 산출물 시각화 |
| `/spec-mix.review`    | `for_review` 레인의 완료된 작업을 검토하고 승인된 작업을 `done`으로 이동     |
| `/spec-mix.accept`    | 병합 전에 포괄적인 검사로 기능 준비 확인     |
| `/spec-mix.merge`     | 정리 옵션으로 기능 브랜치를 main으로 병합 (여러 전략 지원) |

#### 선택적 명령

향상된 품질 및 검증을 위한 추가 명령:

| 명령              | 설명                                                           |
|----------------------|-----------------------------------------------------------------------|
| `/spec-mix.clarify`   | 불충분하게 지정된 영역 명확화 (`/spec-mix.plan` 전에 권장; 이전 `/quizme`) |
| `/spec-mix.analyze`   | 교차 산출물 일관성 및 커버리지 분석 (`/spec-mix.tasks` 후, `/spec-mix.implement` 전에 실행) |
| `/spec-mix.checklist` | 요구사항 완전성, 명확성 및 일관성을 검증하는 사용자 정의 품질 체크리스트 생성 ("영어를 위한 단위 테스트"와 같음) |

### 환경 변수

| 변수         | 설명                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `SPECIFY_FEATURE` | Git 저장소가 아닌 경우 기능 감지 재정의. 기능 디렉토리 이름(예: `001-photo-albums`)으로 설정하여 Git 브랜치를 사용하지 않을 때 특정 기능에서 작업합니다.<br/>**`/spec-mix.plan` 또는 후속 명령을 사용하기 전에 작업 중인 에이전트의 컨텍스트에서 설정해야 합니다.** |

## 📚 핵심 철학

Spec-Driven Development는 다음을 강조하는 구조화된 프로세스입니다:

- 명세가 "*어떻게*" 전에 "*무엇을*"을 정의하는 **의도 기반 개발**

- 가드레일 및 조직 원칙을 사용한 **풍부한 명세 생성**

- 프롬프트에서 원샷 코드 생성이 아닌 **다단계 개선**

- 명세 해석을 위한 고급 AI 모델 기능에 대한 **높은 의존도**

## 🌟 개발 단계

| 단계 | 초점 | 주요 활동 |
|-------|-------|----------------|
| **0-to-1 개발** ("Greenfield") | 처음부터 생성 | <ul><li>높은 수준의 요구사항으로 시작</li><li>명세 생성</li><li>구현 단계 계획</li><li>프로덕션 준비 애플리케이션 구축</li></ul> |
| **창의적 탐색** | 병렬 구현 | <ul><li>다양한 솔루션 탐색</li><li>여러 기술 스택 및 아키텍처 지원</li><li>UX 패턴 실험</li></ul> |
| **반복적 개선** ("Brownfield") | Brownfield 현대화 | <ul><li>기능을 반복적으로 추가</li><li>레거시 시스템 현대화</li><li>프로세스 적응</li></ul> |

## 🎯 실험적 목표

우리의 연구 및 실험은 다음에 초점을 맞춥니다:

### 기술 독립성

- 다양한 기술 스택을 사용하여 애플리케이션 생성

- Spec-Driven Development가 특정 기술, 프로그래밍 언어 또는 프레임워크에 국한되지 않는 프로세스라는 가설 검증

### 엔터프라이즈 제약

- 미션 크리티컬 애플리케이션 개발 시연

- 조직 제약 통합 (클라우드 제공업체, 기술 스택, 엔지니어링 관행)

- 엔터프라이즈 디자인 시스템 및 규정 준수 요구사항 지원

### 사용자 중심 개발

- 다양한 사용자 집단 및 선호도를 위한 애플리케이션 구축

- 다양한 개발 접근 방식 지원 (vibe-coding에서 AI 네이티브 개발까지)

### 창의적 및 반복적 프로세스

- 병렬 구현 탐색 개념 검증

- 강력한 반복적 기능 개발 워크플로우 제공

- 업그레이드 및 현대화 작업을 처리하도록 프로세스 확장

## 🔧 전제 조건

- **Linux/macOS/Windows**

- [지원되는](#-지원되는-ai-에이전트) AI 코딩 에이전트

- 패키지 관리를 위한 [uv](https://docs.astral.sh/uv/)

- [Python 3.11+](https://www.python.org/downloads/)

- [Git](https://git-scm.com/downloads)

에이전트에 문제가 발생하면 통합을 개선할 수 있도록 이슈를 열어주세요.

## 📖 더 알아보기

- **[완전한 Spec-Driven Development 방법론](./spec-driven.md)** - 전체 프로세스에 대한 심층 분석

- **[상세 워크스루](#-상세-프로세스)** - 단계별 구현 가이드

---

## 📋 상세 프로세스

<details>
<summary>단계별 워크스루를 확장하려면 클릭하세요</summary>

Spec Mix CLI를 사용하여 프로젝트를 부트스트랩할 수 있으며, 이는 환경에 필요한 아티팩트를 가져옵니다. 실행:

```bash
spec-mix init <project_name>

```

또는 현재 디렉토리에서 초기화:

```bash
spec-mix init .
# 또는 --here 플래그 사용
spec-mix init --here
# 디렉토리에 이미 파일이 있을 때 확인 건너뛰기
spec-mix init . --force
# 또는
spec-mix init --here --force

```

사용 중인 AI 에이전트를 선택하라는 메시지가 표시됩니다. 터미널에서 직접 미리 지정할 수도 있습니다:

```bash
spec-mix init <project_name> --ai claude
spec-mix init <project_name> --ai gemini
spec-mix init <project_name> --ai copilot

# 또는 현재 디렉토리에서:
spec-mix init . --ai claude
spec-mix init . --ai codex

# 또는 --here 플래그 사용
spec-mix init --here --ai claude
spec-mix init --here --ai codex

# 비어 있지 않은 현재 디렉토리로 강제 병합
spec-mix init . --force --ai claude

# 또는
spec-mix init --here --force --ai claude

```

CLI는 Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI 또는 Amazon Q Developer CLI가 설치되어 있는지 확인합니다. 설치되어 있지 않거나 올바른 도구를 확인하지 않고 템플릿을 가져오려는 경우 명령에 `--ignore-agent-tools`를 사용하세요:

```bash
spec-mix init <project_name> --ai claude --ignore-agent-tools

```

### **1단계:** 프로젝트 원칙 수립

프로젝트 폴더로 이동하여 AI 에이전트를 실행하세요. 예제에서는 `claude`를 사용합니다.
`/spec-mix.constitution`, `/spec-mix.specify`, `/spec-mix.plan`, `/spec-mix.tasks` 및 `/spec-mix.implement` 명령을 사용할 수 있다면 올바르게 구성된 것입니다.

첫 번째 단계는 `/spec-mix.constitution` 명령을 사용하여 프로젝트의 지배 원칙을 수립하는 것입니다. 이는 모든 후속 개발 단계에서 일관된 의사 결정을 보장하는 데 도움이 됩니다:

```text
/spec-mix.constitution 코드 품질, 테스팅 표준, 사용자 경험 일관성 및 성능 요구사항에 중점을 둔 원칙을 만드세요. 이러한 원칙이 기술 결정 및 구현 선택을 어떻게 안내해야 하는지에 대한 거버넌스를 포함하세요.

```

이 단계는 AI 에이전트가 명세, 계획 및 구현 단계에서 참조할 프로젝트의 기본 가이드라인으로 `.spec-mix/memory/constitution.md` 파일을 생성하거나 업데이트합니다.

### **2단계:** 프로젝트 명세 생성

프로젝트 원칙이 수립되면 이제 기능 명세를 생성할 수 있습니다. `/spec-mix.specify` 명령을 사용한 다음 개발하려는 프로젝트에 대한 구체적인 요구사항을 제공하세요.

>[!IMPORTANT]
>무엇을 구축하려고 하는지와 그 이유에 대해 가능한 한 명시적으로 설명하세요. **이 시점에서는 기술 스택에 집중하지 마세요**.

예제 프롬프트:

```text
Taskify, 팀 생산성 플랫폼을 개발하세요. 사용자가 프로젝트를 만들고, 팀원을 추가하고, 작업을 할당하고,
칸반 스타일로 보드 간에 작업을 댓글 달고 이동할 수 있어야 합니다. 이 기능의 초기 단계에서 "Create Taskify"라고
부르겠습니다. 여러 사용자가 있지만 사용자는 미리 선언되어 미리 정의됩니다. 두 가지 범주로 5명의 사용자를 원합니다.
한 명의 제품 관리자와 네 명의 엔지니어입니다. 세 개의 다른 샘플 프로젝트를 만들겠습니다. "To Do", "In Progress",
"In Review" 및 "Done"과 같은 각 작업 상태에 대한 표준 칸반 열이 있을 것입니다. 이것은 기본 기능이 설정되어
있는지 확인하기 위한 첫 번째 테스트이므로 이 애플리케이션에는 로그인이 없습니다. 작업 카드에 대한 UI의 각 작업에
대해 칸반 작업 보드의 다른 열 간에 작업의 현재 상태를 변경할 수 있어야 합니다. 특정 카드에 대해 무제한 댓글을 남길
수 있어야 합니다. 해당 작업 카드에서 유효한 사용자 중 한 명을 할당할 수 있어야 합니다. Taskify를 처음 실행하면
선택할 다섯 명의 사용자 목록이 제공됩니다. 비밀번호가 필요하지 않습니다. 사용자를 클릭하면 프로젝트 목록을 표시하는
메인 뷰로 이동합니다. 프로젝트를 클릭하면 해당 프로젝트의 칸반 보드가 열립니다. 열이 표시됩니다. 다른 열 사이에서
카드를 드래그 앤 드롭할 수 있습니다. 현재 로그인한 사용자인 자신에게 할당된 카드는 다른 모든 카드와 다른 색상으로
표시되므로 자신의 카드를 빠르게 볼 수 있습니다. 자신이 작성한 댓글은 편집할 수 있지만 다른 사람이 작성한 댓글은
편집할 수 없습니다. 자신이 작성한 댓글은 삭제할 수 있지만 다른 사람이 작성한 댓글은 삭제할 수 없습니다.

```

이 프롬프트를 입력한 후 Claude Code가 계획 및 명세 초안 프로세스를 시작하는 것을 볼 수 있습니다. Claude Code는 또한 저장소를 설정하기 위해 일부 내장 스크립트를 트리거합니다.

이 단계가 완료되면 새 브랜치(예: `001-create-taskify`)와 `specs/001-create-taskify` 디렉토리에 새 명세가 생성됩니다.

생성된 명세에는 템플릿에 정의된 대로 사용자 스토리 및 기능 요구사항 세트가 포함되어야 합니다.

이 단계에서 프로젝트 폴더 내용은 다음과 유사해야 합니다:

```text
└── .specify
    ├── memory
    │  └── constitution.md
    ├── scripts
    │  ├── check-prerequisites.sh
    │  ├── common.sh
    │  ├── create-new-feature.sh
    │  ├── setup-plan.sh
    │  └── update-claude-md.sh
    ├── specs
    │  └── 001-create-taskify
    │      └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md

```

### **3단계:** 기능 명세 명확화 (계획 전 필수)

기준 명세가 생성되면 첫 번째 시도에서 제대로 캡처되지 않은 요구사항을 명확하게 할 수 있습니다.

기술 계획을 만들기 **전에** 구조화된 명확화 워크플로우를 실행하여 다운스트림 재작업을 줄여야 합니다.

선호하는 순서:

1. `/spec-mix.clarify` 사용 (구조화됨) – 명확화 섹션에 답변을 기록하는 순차적, 커버리지 기반 질문.
2. 여전히 모호하게 느껴지는 경우 임시 자유 형식 개선으로 선택적으로 후속 조치.

의도적으로 명확화를 건너뛰려는 경우(예: 스파이크 또는 탐색적 프로토타입), 에이전트가 누락된 명확화에서 차단되지 않도록 명시적으로 명시하세요.

예제 자유 형식 개선 프롬프트 (`/spec-mix.clarify` 후에도 여전히 필요한 경우):

```text
생성하는 각 샘플 프로젝트 또는 프로젝트에 대해 각각에 대해 5개에서 15개 사이의 가변 작업 수가 있어야 하며
완료의 다양한 상태로 무작위로 분산되어야 합니다. 각 완료 단계에 최소한 하나의 작업이 있는지 확인하세요.

```

또한 Claude Code에게 **검토 및 수락 체크리스트**를 검증하고 요구사항을 충족하는 검증된/통과된 항목을 체크하고 그렇지 않은 항목은 체크하지 않은 상태로 두도록 요청해야 합니다. 다음 프롬프트를 사용할 수 있습니다:

```text
검토 및 수락 체크리스트를 읽고 기능 명세가 기준을 충족하면 체크리스트의 각 항목을 체크하세요. 그렇지 않으면 비워 두세요.

```

Claude Code와의 상호 작용을 명세에 대한 질문을 명확하게 하고 묻는 기회로 사용하는 것이 중요합니다 - **첫 번째 시도를 최종으로 취급하지 마세요**.

### **4단계:** 계획 생성

이제 기술 스택 및 기타 기술 요구사항에 대해 구체적으로 설명할 수 있습니다. 다음과 같은 프롬프트와 함께 프로젝트 템플릿에 내장된 `/spec-mix.plan` 명령을 사용할 수 있습니다:

```text
.NET Aspire를 사용하여 생성하고 데이터베이스로 Postgres를 사용합니다. 프론트엔드는 드래그 앤 드롭 작업 보드,
실시간 업데이트가 있는 Blazor 서버를 사용해야 합니다. 프로젝트 API, 작업 API 및 알림 API로 생성된 REST API가
있어야 합니다.

```

이 단계의 출력에는 여러 구현 세부정보 문서가 포함되며 디렉토리 트리는 다음과 유사합니다:

```text
.
├── CLAUDE.md
├── memory
│  └── constitution.md
├── scripts
│  ├── check-prerequisites.sh
│  ├── common.sh
│  ├── create-new-feature.sh
│  ├── setup-plan.sh
│  └── update-claude-md.sh
├── specs
│  └── 001-create-taskify
│      ├── contracts
│      │  ├── api-spec.json
│      │  └── signalr-spec.md
│      ├── data-model.md
│      ├── plan.md
│      ├── quickstart.md
│      ├── research.md
│      └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md

```

`research.md` 문서를 확인하여 지침에 따라 올바른 기술 스택이 사용되는지 확인하세요. 구성 요소가 눈에 띄는 경우 Claude Code에 이를 개선하도록 요청하거나 사용하려는 플랫폼/프레임워크의 로컬 설치 버전(예: .NET)을 확인하도록 할 수도 있습니다.

또한 빠르게 변화하는 것(예: .NET Aspire, JS 프레임워크)인 경우 선택한 기술 스택에 대한 세부정보를 조사하도록 Claude Code에 요청할 수 있습니다:

```text
구현 계획 및 구현 세부정보를 살펴보고 .NET Aspire가 빠르게 변화하는 라이브러리이므로 추가 연구가 도움이 될 수
있는 영역을 찾고 싶습니다. 추가 연구가 필요하다고 식별한 영역에 대해 이 Taskify 애플리케이션에서 사용할 특정 버전에
대한 추가 세부정보로 연구 문서를 업데이트하고 웹에서 연구를 사용하여 세부정보를 명확하게 하기 위해 병렬 연구 작업을
생성하기를 원합니다.

```

이 프로세스 중에 Claude Code가 잘못된 것을 조사하는 데 막히는 것을 발견할 수 있습니다 - 다음과 같은 프롬프트로 올바른 방향으로 유도할 수 있습니다:

```text
이것을 일련의 단계로 나누어야 한다고 생각합니다. 먼저 구현 중에 수행해야 하는 작업 목록을 식별하되 확실하지 않거나
추가 연구가 도움이 될 것입니다. 해당 작업 목록을 작성하세요. 그런 다음 이러한 각 작업에 대해 별도의 연구 작업을 생성하여
최종 결과가 매우 구체적인 모든 작업을 병렬로 조사하는 것입니다. 내가 본 것은 .NET Aspire를 일반적으로 조사하는 것처럼
보였고 이 경우에 많은 도움이 되지 않을 것 같습니다. 그것은 너무 타겟이 없는 연구입니다. 연구는 특정 타겟 질문을 해결하는
데 도움이 되어야 합니다.

```

>[!NOTE]
>Claude Code는 지나치게 열심히 요청하지 않은 구성 요소를 추가할 수 있습니다. 변경의 근거와 출처를 명확히 하도록 요청하세요.

### **5단계:** Claude Code가 계획을 검증하도록 하기

계획이 준비되면 Claude Code가 누락된 부분이 없는지 확인하도록 해야 합니다. 다음과 같은 프롬프트를 사용할 수 있습니다:

```text
이제 구현 계획 및 구현 세부정보 파일을 감사하기를 원합니다. 수행해야 하는 일련의 작업이 있는지 여부를 결정하는
데 중점을 두고 읽어보세요. 여기에 충분한 것이 있는지 모르기 때문입니다. 예를 들어 핵심 구현을 볼 때 각 단계를
안내할 때 정보를 찾을 수 있는 구현 세부정보의 적절한 위치를 핵심 구현 또는 개선에서 참조하는 것이 유용할 것입니다.

```

이는 구현 계획을 개선하는 데 도움이 되며 Claude Code가 계획 주기에서 놓친 잠재적인 맹점을 피하는 데 도움이 됩니다. 초기 개선 패스가 완료되면 구현을 시작하기 전에 Claude Code에 체크리스트를 다시 한 번 확인하도록 요청하세요.

또한 [GitHub CLI](https://docs.github.com/en/github-cli/github-cli)가 설치되어 있는 경우 Claude Code에 현재 브랜치에서 `main`으로 자세한 설명과 함께 풀 리퀘스트를 만들어 노력이 제대로 추적되도록 요청할 수도 있습니다.

>[!NOTE]
>에이전트가 구현하기 전에 Claude Code에 세부정보를 교차 확인하여 과도하게 엔지니어링된 부분이 있는지 확인하는 것도 가치가 있습니다(기억하세요 - 과도하게 열심일 수 있습니다). 과도하게 엔지니어링된 구성 요소 또는 결정이 존재하는 경우 Claude Code에 이를 해결하도록 요청할 수 있습니다. Claude Code가 계획을 수립할 때 반드시 준수해야 하는 기본 부분으로 [constitution](base/memory/constitution.md)을 따르는지 확인하세요.

### **6단계:** /spec-mix.tasks로 작업 분해 생성

구현 계획이 검증되면 이제 올바른 순서로 실행할 수 있는 특정 실행 가능한 작업으로 계획을 세분화할 수 있습니다. `/spec-mix.tasks` 명령을 사용하여 구현 계획에서 자동으로 상세한 작업 분해를 생성하세요:

```text
/spec-mix.tasks

```

이 단계는 기능 명세 디렉토리에 다음을 포함하는 `tasks.md` 파일을 생성합니다:

- **사용자 스토리별로 구성된 작업 분해** - 각 사용자 스토리는 자체 작업 세트가 있는 별도의 구현 단계가 됩니다

- **종속성 관리** - 작업은 구성 요소 간 종속성을 존중하도록 순서가 지정됩니다(예: 서비스 전의 모델, 엔드포인트 전의 서비스)

- **병렬 실행 마커** - 병렬로 실행할 수 있는 작업은 개발 워크플로우를 최적화하기 위해 `[P]`로 표시됩니다

- **파일 경로 사양** - 각 작업에는 구현이 발생해야 하는 정확한 파일 경로가 포함됩니다

- **테스트 주도 개발 구조** - 테스트가 요청되면 테스트 작업이 포함되고 구현 전에 작성되도록 순서가 지정됩니다

- **체크포인트 검증** - 각 사용자 스토리 단계에는 독립적인 기능을 검증하기 위한 체크포인트가 포함됩니다

생성된 tasks.md는 `/spec-mix.implement` 명령에 대한 명확한 로드맵을 제공하여 코드 품질을 유지하고 사용자 스토리의 점진적 전달을 허용하는 체계적인 구현을 보장합니다.

### **7단계:** 구현

준비가 되면 `/spec-mix.implement` 명령을 사용하여 구현 계획을 실행하세요:

```text
/spec-mix.implement

```

`/spec-mix.implement` 명령은:

- 모든 전제 조건이 준비되어 있는지 검증합니다(constitution, spec, plan 및 tasks)

- `tasks.md`에서 작업 분해를 구문 분석합니다

- 종속성 및 병렬 실행 마커를 존중하면서 올바른 순서로 작업을 실행합니다

- 작업 계획에 정의된 TDD 접근 방식을 따릅니다

- 진행 상황 업데이트를 제공하고 오류를 적절하게 처리합니다

>[!IMPORTANT]
>AI 에이전트는 로컬 CLI 명령(예: `dotnet`, `npm` 등)을 실행합니다 - 필요한 도구가 컴퓨터에 설치되어 있는지 확인하세요.

구현이 완료되면 애플리케이션을 테스트하고 CLI 로그에 표시되지 않을 수 있는 런타임 오류(예: 브라우저 콘솔 오류)를 해결하세요. 해결을 위해 이러한 오류를 AI 에이전트에 복사하여 붙여넣을 수 있습니다.

</details>

---

## 🔍 문제 해결

### Linux에서 Git Credential Manager

Linux에서 Git 인증에 문제가 있는 경우 Git Credential Manager를 설치할 수 있습니다:

```bash
#!/usr/bin/env bash
set -e
echo "Git Credential Manager v2.6.1 다운로드 중..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Git Credential Manager 설치 중..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Git이 GCM을 사용하도록 구성 중..."
git config --global credential.helper manager
echo "정리 중..."
rm gcm-linux_amd64.2.6.1.deb

```

## 👥 메인테이너

- Den Delimarsky ([@localden](https://github.com/localden))

- John Lam ([@jflam](https://github.com/jflam))

## 💬 지원

지원이 필요하면:

- **핵심 Spec Kit 이슈**: 업스트림 저장소에서 [GitHub 이슈](https://github.com/github/spec-kit/issues/new)를 여세요

- **다국어 또는 포크 관련 이슈**: 이 저장소에서 이슈를 여세요

버그 보고서, 기능 요청 및 Spec-Driven Development 사용에 대한 질문을 환영합니다.

## 🙏 감사의 말

이 프로젝트는 [John Lam](https://github.com/jflam)의 작업과 연구에 크게 영향을 받았으며 기반을 두고 있습니다.

## 🔀 Fork 정보

이것은 개인 및 팀 사용을 위해 유지 관리되는 원본 [github/spec-kit](https://github.com/github/spec-kit) 프로젝트의 포크로, 추가 기능이 있습니다:

### 이 포크에 추가된 기능

- **🌍 다국어 지원 (i18n)**: 완전한 국제화 인프라

  - 완전한 한국어 번역

  - 언어 관리 명령 (`spec-mix lang`)

  - 시스템 로케일 기반 자동 언어 감지

  - 더 많은 언어 추가를 위한 확장 가능한 아키텍처

- **🎯 미션 시스템**: 도메인별 워크플로우 및 템플릿

  - 소프트웨어 개발 미션 (코드 품질, 테스팅, UX 중점)

  - 심층 연구 미션 (증거 기반 분석, 리서치 방법론)

  - 미션별 템플릿, 명령 및 검증 규칙

  - 다국어 미션 지원

  - 미션 관리 명령 (`spec-mix mission`)

- **📊 웹 대시보드**: 시각적 모니터링 및 탐색

  - 작업 통계가 있는 실시간 기능 개요

  - 대화형 칸반 보드 (planned/doing/for_review/done)

  - 마크다운 렌더링이 있는 산출물 뷰어

  - 다중 워크트리 지원

  - 자동 새로고침 (2초 간격)

  - 다국어 UI (시스템 로케일에 적응)

- **🔄 향상된 워크플로우**: 고급 작업 관리

  - 기능 격리를 위한 Git 워크트리 통합

  - 작업 레인 시스템 (칸반 스타일)

  - 검토, 수락 및 병합 명령

  - 프론트매터 메타데이터를 사용한 작업 패키지 (WPxx) 추적

### 업스트림 동기화

이 포크는 추가 기능을 유지하면서 업스트림 저장소와 동기화된 상태를 유지하는 것을 목표로 합니다. 이러한 수정 없이 원본 버전을 원하시면 [업스트림 저장소](https://github.com/github/spec-kit)를 방문하세요.

### 기여

다음과 관련된 기여:

- **핵심 Spec Kit 기능**: [업스트림 저장소](https://github.com/github/spec-kit)에 제출하세요

- **다국어 지원 또는 포크별 기능**: 이 저장소에 제출하세요

### 업스트림 크레딧

원본 프로젝트는 다음에 의해 유지 관리됩니다:

- Den Delimarsky ([@localden](https://github.com/localden))

- John Lam ([@jflam](https://github.com/jflam))

## 📄 라이선스

이 프로젝트는 MIT 오픈소스 라이선스 조건에 따라 라이선스가 부여됩니다. 전체 조건은 [LICENSE](./LICENSE) 파일을 참조하세요.
