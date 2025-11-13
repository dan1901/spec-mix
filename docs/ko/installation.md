# 설치 가이드

## 필수 요구사항

- **Linux/macOS** (또는 Windows; WSL 없이 PowerShell 스크립트 지원)
- AI 코딩 에이전트: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Codebuddy CLI](https://www.codebuddy.ai/cli) 또는 [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- 패키지 관리를 위한 [uv](https://docs.astral.sh/uv/)
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 설치

### 새 프로젝트 초기화

가장 쉬운 시작 방법은 새 프로젝트를 초기화하는 것입니다:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <PROJECT_NAME>
```

또는 현재 디렉토리에 초기화:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init .
# 또는 --here 플래그 사용
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init --here
```

### AI 에이전트 지정

초기화 시 AI 에이전트를 미리 지정할 수 있습니다:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --ai claude
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --ai gemini
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --ai copilot
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --ai codebuddy
```

### 스크립트 유형 지정 (Shell vs PowerShell)

모든 자동화 스크립트는 이제 Bash (`.sh`)와 PowerShell (`.ps1`) 버전을 모두 제공합니다.

자동 동작:

- Windows 기본값: `ps`
- 기타 OS 기본값: `sh`
- 대화형 모드: `--script`를 전달하지 않으면 프롬프트가 표시됩니다

특정 스크립트 유형 강제:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --script sh
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --script ps
```

### 에이전트 도구 확인 무시

도구 확인 없이 템플릿을 가져오고 싶다면:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --ai claude --ignore-agent-tools
```

### 언어 선택

프로젝트 언어를 지정할 수 있습니다:

```bash
# 한국어로 초기화
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --language ko

# 영어 (기본값)
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --language en
```

### 미션 선택

프로젝트 유형에 맞는 미션을 선택하세요:

```bash
# 소프트웨어 개발 (기본값)
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --mission software-dev

# 연구 프로젝트
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init <project_name> --mission research
```

### 모든 옵션 결합

```bash
# 한국어 연구 프로젝트를 Claude로
uvx --from git+https://github.com/dan1901/spec-mix.git spec-mix init my-research \
  --language ko \
  --mission research \
  --ai claude \
  --script sh
```

## 검증

초기화 후 AI 에이전트에서 다음 명령어들을 사용할 수 있어야 합니다:

- `/spec-mix.specify` - 사양 생성
- `/spec-mix.plan` - 구현 계획 생성
- `/spec-mix.tasks` - 실행 가능한 작업으로 분해

`.spec-mix/scripts` 디렉토리에는 `.sh`와 `.ps1` 스크립트가 모두 포함됩니다.

올바르게 구성되었는지 확인하려면 `/spec-mix.constitution`, `/spec-mix.specify`, `/spec-mix.plan`, `/spec-mix.tasks`, `/spec-mix.implement` 명령어가 사용 가능한지 확인하세요.

## 도구로 설치

프로젝트에서 `spec-mix`를 전역적으로 사용하려면:

```bash
uv tool install spec-mix --from git+https://github.com/dan1901/spec-mix.git
```

설치 후:

```bash
spec-mix --help
spec-mix init my-project
spec-mix lang list
spec-mix mission list
spec-mix dashboard
```

## Git 자격 증명 (Linux)

Linux에서 Git 인증에 문제가 있는 경우 Git Credential Manager를 설치할 수 있습니다:

```bash
# Ubuntu/Debian
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
sudo dpkg -i gcm-linux_amd64.2.6.1.deb

# 구성
git-credential-manager configure
```

## 문제 해결

### "command not found: uvx"

uv를 설치하세요:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "No such option: --language"

최신 버전을 사용하고 있는지 확인하세요:

```bash
uvx --from git+https://github.com/dan1901/spec-mix.git@main spec-mix init --help
```

### 명령어가 AI 에이전트에 나타나지 않음

1. 올바른 디렉토리에 초기화했는지 확인
2. AI 에이전트 재시작
3. 에이전트별 명령어 디렉토리 확인:
   - Claude: `.claude/commands/`
   - Copilot: `.github/prompts/`
   - Gemini: `.gemini/commands/`

### 언어 팩을 찾을 수 없음

지원되는 언어인지 확인:

```bash
spec-mix lang list
```

현재 지원: `en`, `ko`

## 다음 단계

- [빠른 시작](quickstart.md) - 첫 번째 기능 만들기
- [향상된 기능](features.md) - 모든 Spec Mix 기능 살펴보기
- [다국어 가이드](i18n.md) - 언어 관리
- [미션 시스템](missions.md) - 미션 선택 및 사용
