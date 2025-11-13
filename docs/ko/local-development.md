# 로컬 개발 가이드

이 가이드는 릴리스를 게시하거나 먼저 `main`에 커밋하지 않고 `spec-mix` CLI를 로컬에서 반복하는 방법을 보여줍니다.

> 스크립트는 이제 Bash(`.sh`)와 PowerShell(`.ps1`) 버전을 모두 제공합니다. CLI는 `--script sh|ps`를 전달하지 않는 한 OS를 기반으로 자동 선택합니다.

## 1. 클론 및 브랜치 전환

```bash
git clone https://github.com/dan1901/spec-mix.git
cd spec-mix
# 기능 브랜치에서 작업
git checkout -b your-feature-branch
```

## 2. CLI 직접 실행 (가장 빠른 피드백)

아무것도 설치하지 않고 모듈 진입점을 통해 CLI를 실행할 수 있습니다:

```bash
# 저장소 루트에서
python -m src.specmix --help
python -m src.specmix init demo-project --ai claude --ignore-agent-tools --script sh
```

스크립트 파일 스타일 호출을 선호하는 경우 (shebang 사용):

```bash
python src/specmix/__init__.py init demo-project --script ps
```

## 3. 편집 가능한 설치 사용 (격리된 환경)

`uv`를 사용하여 격리된 환경을 만들면 최종 사용자가 받는 것과 정확히 같이 종속성이 해결됩니다:

```bash
# 가상 환경 생성 및 활성화 (uv가 자동으로 .venv 관리)
uv venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1

# 편집 가능한 모드로 프로젝트 설치
uv pip install -e .

# 이제 'spec-mix' 진입점을 사용할 수 있습니다
spec-mix --help
```

편집 가능한 모드이므로 코드 편집 후 재실행할 때 재설치가 필요하지 않습니다.

## 4. Git에서 uvx로 직접 호출 (현재 브랜치)

`uvx`는 로컬 경로(또는 Git 참조)에서 실행하여 사용자 흐름을 시뮬레이션할 수 있습니다:

```bash
uvx --from . spec-mix init demo-uvx --ai copilot --ignore-agent-tools --script sh
```

병합하지 않고 특정 브랜치를 uvx로 가리킬 수도 있습니다:

```bash
# 먼저 작업 브랜치를 푸시
git push origin your-feature-branch
uvx --from git+https://github.com/dan1901/spec-mix.git@your-feature-branch spec-mix init demo-branch-test --script ps
```

### 4a. 절대 경로 uvx (어디서나 실행)

다른 디렉토리에 있는 경우 `.` 대신 절대 경로를 사용하세요:

```bash
uvx --from /path/to/spec-mix spec-mix --help
uvx --from /path/to/spec-mix spec-mix init demo-anywhere --ai copilot --ignore-agent-tools --script sh
```

편의를 위해 환경 변수 설정:

```bash
export SPEC_MIX_SRC=/path/to/spec-mix
uvx --from "$SPEC_MIX_SRC" spec-mix init demo-env --ai copilot --ignore-agent-tools --script ps
```

(선택 사항) 셸 함수 정의:

```bash
spec-mix-dev() { uvx --from /path/to/spec-mix spec-mix "$@"; }
# 그런 다음
spec-mix-dev --help
```

## 5. 스크립트 권한 로직 테스트

`init`을 실행한 후 POSIX 시스템에서 셸 스크립트가 실행 가능한지 확인하세요:

```bash
ls -l scripts | grep .sh
# 소유자 실행 비트를 예상 (예: -rwxr-xr-x)
```

Windows에서는 대신 `.ps1` 스크립트를 사용합니다 (chmod 필요 없음).

## 6. 린트 / 기본 검사 실행 (직접 추가)

현재 번들로 제공되는 린트 구성은 없지만 가져오기 가능성을 빠르게 검사할 수 있습니다:

```bash
python -c "import specmix; print('Import OK')"
```

## 7. 로컬로 휠 빌드 (선택 사항)

게시하기 전에 패키징 검증:

```bash
uv build
ls dist/
```

필요한 경우 빌드된 아티팩트를 새로운 임시 환경에 설치하세요.

## 8. 임시 작업 공간 사용

더러운 디렉토리에서 `init --here`를 테스트할 때 임시 작업 공간을 만드세요:

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test
python -m src.specmix init --here --ai claude --ignore-agent-tools --script sh  # 저장소를 여기에 복사한 경우
```

또는 더 가벼운 샌드박스를 원하는 경우 수정된 CLI 부분만 복사하세요.

## 9. 네트워크 / TLS 건너뛰기 디버그

실험하는 동안 TLS 검증을 우회해야 하는 경우:

```bash
spec-mix check --skip-tls
spec-mix init demo --skip-tls --ai gemini --ignore-agent-tools --script ps
```

(로컬 실험용으로만 사용하세요.)

## 10. 빠른 편집 루프 요약

| 작업 | 명령 |
|------|------|
| CLI 직접 실행 | `python -m src.specmix --help` |
| 편집 가능한 설치 | `uv pip install -e .` 그런 다음 `spec-mix ...` |
| 로컬 uvx 실행 (저장소 루트) | `uvx --from . spec-mix ...` |
| 로컬 uvx 실행 (절대 경로) | `uvx --from /path/to/spec-mix spec-mix ...` |
| Git 브랜치 uvx | `uvx --from git+URL@branch spec-mix ...` |
| 휠 빌드 | `uv build` |

## 11. 정리

빌드 아티팩트 / 가상 환경을 빠르게 제거:

```bash
rm -rf .venv dist build *.egg-info
```

## 12. 일반적인 문제

| 증상 | 해결 방법 |
|------|----------|
| `ModuleNotFoundError: typer` | `uv pip install -e .` 실행 |
| 스크립트가 실행 가능하지 않음 (Linux) | init을 다시 실행하거나 `chmod +x scripts/*.sh` |
| Git 단계가 건너뜀 | `--no-git`을 전달했거나 Git이 설치되지 않음 |
| 잘못된 스크립트 유형 다운로드 | `--script sh` 또는 `--script ps`를 명시적으로 전달 |
| 기업 네트워크의 TLS 오류 | `--skip-tls` 시도 (프로덕션용 아님) |

## 13. 다음 단계

- 문서를 업데이트하고 수정된 CLI를 사용하여 빠른 시작을 실행
- 만족하면 PR 열기
- (선택 사항) 변경 사항이 `main`에 적용되면 릴리스 태그
