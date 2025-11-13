# Spec Mix 향상된 기능

Spec Mix는 다국어 개발, 미션 기반 워크플로 및 시각적 프로젝트 관리를 위한 강력한 기능으로 원래 Spec Kit를 확장합니다.

## 개요

이 포크는 세 가지 주요 기능 세트를 추가합니다:

1. **다국어 지원 (i18n)** - 완전한 국제화 지원
2. **미션 시스템** - 도메인별 워크플로 템플릿
3. **웹 대시보드** - 시각적 프로젝트 관리 인터페이스

## 다국어 지원 (i18n)

전체 문서는 [다국어 가이드](i18n.md)에서 확인할 수 있습니다

### 주요 기능

- **여러 언어 팩** - 현재 영어와 한국어 지원
- **로케일별 명령어** - 선호하는 언어의 슬래시 명령어
- **언어별 미션 템플릿** - 현지화된 워크플로 템플릿
- **CLI 언어 전환** - 쉬운 언어 관리

### 빠른 시작

```bash
# 사용 가능한 언어 목록
spec-mix lang list

# 언어 설정
spec-mix lang set ko

# 언어로 프로젝트 초기화
spec-mix init my-project --language ko
```

## 미션 시스템

미션 시스템은 다양한 유형의 프로젝트에 최적화된 도메인별 워크플로 템플릿을 제공합니다.

### 사용 가능한 미션

#### 소프트웨어 개발 미션

다음을 포함하는 소프트웨어 애플리케이션 구축에 최적화:

- 기능 사양 템플릿
- 구현 계획 워크플로
- 작업 분해 구조
- 코드 리뷰 체크리스트
- 테스트 가이드라인

```bash
spec-mix init my-app --mission software-dev
```

#### 연구 미션

다음을 포함하는 연구 프로젝트를 위해 설계:

- 연구 질문 템플릿
- 분석 워크플로
- 결과 문서화
- 문헌 검토 구조
- 데이터 분석 가이드라인

```bash
spec-mix init my-research --mission research
```

### 미션 구조

각 미션에는 다음이 포함됩니다:

```text
missions/[mission-name]/
├── commands/           # 미션별 슬래시 명령어
│   ├── constitution.md
│   ├── specify.md
│   ├── plan.md
│   └── ...
├── templates/         # 문서 템플릿
│   ├── spec-template.md
│   ├── plan-template.md
│   └── ...
└── constitution/      # 미션 가이드라인
    └── constitution-template.md
```

### 미션 전환

기존 프로젝트에서 미션을 전환할 수 있습니다:

```bash
spec-mix mission list              # 사용 가능한 미션 목록
spec-mix mission set research      # 연구 미션으로 전환
```

## 웹 대시보드

대시보드는 사양 주도 개발 워크플로를 관리하기 위한 시각적 인터페이스를 제공합니다.

### 기능

- **기능 개요** - `specs/`의 모든 기능에 대한 시각적 목록
- **상태 추적** - 기능 진행 상황을 한눈에 확인
- **문서 미리보기** - 사양, 계획 및 작업 읽기
- **마크다운 렌더링** - 아름답게 포맷된 문서
- **실시간 업데이트** - 파일 변경 시 자동 새로고침

### 대시보드 시작

```bash
# 대시보드 시작 (기본 포트 8080)
spec-mix dashboard

# 사용자 정의 포트
spec-mix dashboard --port 3000

# 사용자 정의 호스트
spec-mix dashboard --host 0.0.0.0 --port 8080
```

### 대시보드 뷰

#### 기능 목록

다음이 포함된 모든 기능 표시:

- 기능 번호 및 이름
- 현재 상태 (`spec.md`에서)
- 사양, 계획 및 작업에 대한 빠른 링크
- 색상으로 구분된 상태 표시기

#### 문서 뷰어

모든 사양 문서 보기:

- 전체 마크다운 렌더링
- 코드 블록에 대한 구문 강조
- 목차 탐색
- 반응형 디자인

### 대시보드 중지

```bash
# 터미널에서 Ctrl+C 누르기
# 또는 종료 명령 사용
spec-mix dashboard --shutdown
```

## 기능 결합

모든 기능이 원활하게 함께 작동합니다:

```bash
# 대시보드가 있는 한국어 연구 프로젝트 초기화
spec-mix init my-korean-research \
  --language ko \
  --mission research

cd my-korean-research

# 한국어 명령으로 작업 시작
# (AI 에이전트에서)
/spec-mix.specify 연구 질문: 딥러닝 모델의 설명가능성

# 대시보드에서 진행 상황 보기
spec-mix dashboard
```

## 구성

### 언어 구성

언어 설정은 `src/specmix/locales/config.json`에 저장됩니다:

```json
{
  "default_locale": "en",
  "supported_locales": [
    {
      "code": "en",
      "name": "English",
      "native_name": "English",
      "is_default": true
    },
    {
      "code": "ko",
      "name": "Korean",
      "native_name": "한국어"
    }
  ],
  "fallback_locale": "en"
}
```

### 미션 구성

미션은 `src/specmix/locales/[lang]/missions/` 디렉토리에서 자동으로 감지됩니다.

## 직접 추가하기

### 새 언어 추가

1. 로케일 디렉토리 구조 생성:

   ```bash
   mkdir -p src/specmix/locales/[lang-code]/missions/software-dev
   mkdir -p src/specmix/locales/[lang-code]/missions/research
   ```

2. `config.json`에 로케일 추가

3. 명령 파일 및 템플릿 번역

4. `spec-mix lang list`로 테스트

자세한 지침은 [다국어 가이드](i18n.md)를 참조하세요.

### 새 미션 추가

1. 미션 디렉토리 생성:

   ```bash
   mkdir -p src/specmix/locales/en/missions/[mission-name]
   ```

2. 필요한 구조 추가:

   ```text
   [mission-name]/
   ├── commands/
   ├── templates/
   └── constitution/
   ```

3. 기존 미션에서 템플릿 복사 및 사용자 정의

4. `spec-mix mission list`로 테스트

## 모범 사례

### 언어 선택

- 더 나은 협업을 위해 팀의 주요 언어 선택
- 오픈소스 프로젝트에는 영어 권장
- 언어별 용어를 적절하게 사용

### 미션 선택

- **소프트웨어 개발** - 앱, 서비스, 라이브러리, 도구용
- **연구** - 연구, 분석, 실험, 논문용
- 사용자 정의 미션 - 특수 워크플로용

### 대시보드 사용

- 활발한 개발 중에 실행 유지
- 이해관계자 데모에 사용
- 스탠드업 전에 기능 상태 검토
- 팀 멤버와 URL 공유 (`--host 0.0.0.0` 사용 시)

## 문제 해결

### 언어가 표시되지 않음

```bash
# 로케일 파일이 존재하는지 확인
ls src/specmix/locales/

# config.json 확인
cat src/specmix/locales/config.json
```

### 미션 명령어가 작동하지 않음

```bash
# 미션 구조 확인
ls src/specmix/locales/en/missions/[mission-name]/commands/

# 현재 미션 확인
spec-mix mission list
```

### 대시보드가 시작되지 않음

```bash
# 포트 사용 가능 여부 확인
lsof -i :8080

# 다른 포트 시도
spec-mix dashboard --port 8081

# 오류 확인
spec-mix dashboard --verbose
```

## 다음 단계

- [다국어 가이드](i18n.md) - i18n 기능 심층 탐구
- [빠른 시작](quickstart.md) - Spec Mix 시작하기
- [설치](installation.md) - 설치 옵션
