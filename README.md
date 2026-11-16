# design-kit

Claude가 화면을 만들 때 실제 서비스 86곳의 디자인 시스템 중 하나를 골라 그 규칙대로 만들게 하는 스킬입니다.

"대시보드 만들어줘"라고 하면 요청에 맞는 레퍼런스 3개를 추천하고, 고른 레퍼런스의 색, 폰트, 간격, 컴포넌트 규칙을 그대로 적용합니다. "노션 느낌으로", "Linear 스타일로"처럼 직접 지정해도 됩니다.

## 설치

### Claude Code

```
/plugin marketplace add deserite/design-kit
/plugin install design-kit@deserite
```

업데이트는 `/plugin marketplace update deserite`로 받습니다.

### claude.ai · Claude 데스크톱 앱

1. [Releases](https://github.com/deserite/design-kit/releases)에서 `design-kit.zip`을 받습니다.
   Releases에 파일이 없으면 이 레포를 받은 뒤 직접 묶습니다.
   ```bash
   cd skills && zip -r design-kit.zip design-kit
   ```
2. claude.ai 설정의 스킬 메뉴에서 zip 파일을 업로드합니다.

## 사용 예

- `사내 서버 현황 대시보드 만들어줘` → 레퍼런스 후보 3개 추천 → 고르면 그 디자인으로 제작
- `노션 스타일로 회의록 정리 페이지 만들어줘` → notion 레퍼런스로 바로 제작
- `베이스는 vercel, 포인트 색만 stripe로` → 섞어서 적용
- `다른 레퍼런스도 보여줘` → 앞서 보여 준 것을 빼고 다시 추천

## 레퍼런스는 어디서 오나

스킬에는 86개 레퍼런스의 색인(모드, 포인트 색, 특징 한 줄)만 들어 있습니다. 실제 디자인 규칙 파일은 쓸 때 아래 순서로 받아 옵니다.

1. npm 패키지 [`getdesign`](https://www.npmjs.com/package/getdesign)
2. 원본 저장소 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
3. 백업 포크 [deserite/awesome-design-md](https://github.com/deserite/awesome-design-md)

셋 다 막히면 색인 정보만으로 비슷하게 만들고 그 사실을 알려 줍니다.

## 지키는 선

레퍼런스에서는 스타일(색, 타이포, 간격, 레이아웃 원칙)만 빌립니다. 해당 브랜드의 이름, 로고, 제품 사진은 넣지 않고, 그 회사의 실제 사이트나 로그인·결제 화면처럼 보이게 만들지 않습니다.

레퍼런스 파일은 공개된 웹사이트를 분석한 결과라 공식 디자인 시스템이 아니며, 일부 값이 실제와 다를 수 있습니다.

## 구조

```
.claude-plugin/
  marketplace.json   # Claude Code 마켓플레이스 정의
  plugin.json        # 플러그인 정의
skills/design-kit/
  SKILL.md           # 스킬 본문 (원본은 여기)
```

## 출처와 라이선스

- 이 레포: MIT ([LICENSE](LICENSE))
- 레퍼런스 색인의 색상 값과 특징은 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)(MIT, Copyright (c) 2026 VoltAgent)의 DESIGN.md 파일에서 정리했습니다.
- 각 브랜드의 이름과 시각 아이덴티티는 해당 소유자에게 있습니다.
