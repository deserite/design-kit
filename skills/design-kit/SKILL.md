---
name: design-kit
description: 웹페이지·HTML·대시보드·관리 도구 UI·앱 화면·랜딩을 만들 때 실제 사이트 86곳의 DESIGN.md 레퍼런스 중 요청에 맞는 후보를 추천하고, 고른 것의 색·타이포·간격·컴포넌트 규칙대로 만든다. "Linear 느낌으로", "Stripe 스타일", "디자인 레퍼런스 골라줘"나 UI 제작 요청 시 사용.
---

# design-kit — 골라 쓰는 디자인 레퍼런스

화면을 만들 때 "AI가 만든 티 나는 기본 디자인" 대신, 실제 서비스의 디자인 시스템을 분석한 DESIGN.md 하나를 골라 그 규칙대로 만든다.
레퍼런스 원본: VoltAgent `awesome-design-md` (MIT) / getdesign.md 카탈로그. 각 파일은 색 토큰, 타이포 스케일, 간격, 모서리, 그림자, 컴포넌트, Do's & Don'ts, 반응형 규칙을 담고 있다.

## 언제 쓰나

- HTML 페이지, 아티팩트, 대시보드, 어드민·관리 도구, 랜딩, 앱 화면, 보고서형 웹페이지를 만들 때
- 사용자가 특정 서비스 느낌을 말할 때 ("Vercel처럼 깔끔하게", "노션 느낌")
- 기존 화면을 다른 톤으로 리스타일할 때

차트 색 체계는 dataviz 스킬이 있으면 그쪽을 따르고, 페이지 전체 톤만 이 스킬로 맞춘다.

## 작업 순서

### 1. 레퍼런스 정하기

우선순위:
1. 사용자가 slug나 서비스 이름을 말했으면 그것.
2. 작업 폴더(프로젝트 루트)에 `DESIGN.md`가 이미 있으면 그것. 사용자 자신의 디자인이 카탈로그보다 우선이다.
3. 아래 **「내 디자인」** 섹션에 등록된 것이 있고 용도가 맞으면 그것.
4. 없으면 아래 **「전체 색인」 86개를 모두 훑어** 요청에 가장 맞는 후보 3개(많아야 4개)를 골라 AskUserQuestion으로 묻는다.
   - 고르는 기준: ① 화면 성격(대시보드·문서·랜딩·포트폴리오·블로그·앱 등) ② 사용자가 말한 분위기·키워드(따뜻한, 미니멀, 고급, 경쾌한, 다크 등) ③ 정보 밀도(표·데이터가 많은지, 사진·여백 위주인지) ④ 라이트/다크 선호.
   - 후보끼리는 성격이 겹치지 않게 고른다. 예: 같은 흑백 미니멀 3개가 아니라 미니멀 하나, 따뜻한 톤 하나, 다크 하나처럼 서로 다른 방향을 보여 준다.
   - 「용도별 추천」 표는 참고용 출발점일 뿐이다. 요청이 표의 용도와 딱 맞지 않으면(개인 블로그, 포트폴리오, 이벤트 페이지 등) 표에 얽매이지 말고 색인 전체에서 고른다.
   - 각 선택지의 label은 slug, description에는 "모드 · 포인트 색 · 이 요청에 맞는 이유"를 한 줄로 적는다. 가장 잘 맞는 후보를 첫 번째에 두고 "(추천)"을 붙인다.
   - 사용자가 없거나 "알아서"라고 하면 첫 번째 후보로 진행하고 무엇을 썼는지 밝힌다.
   - "다른 것도 보여줘"라고 하면 앞서 보여 준 것을 빼고 다음 후보 3개를 다시 고른다.

섞어 쓰기도 된다: "베이스는 vercel, 포인트 색만 stripe"처럼 지정하면 베이스 파일 전체를 따르고 지정한 토큰만 바꾼다.

### 2. 레퍼런스 파일 불러오기

파일은 스킬에 들어 있지 않고 쓸 때 받아 온다 (파일당 25~35KB).

명령은 맥 터미널과 윈도우 Git Bash(Claude Code 기본 셸) 모두에서 그대로 동작한다. 윈도우 PowerShell에서 직접 돌릴 때만 `/tmp/design-refs` 를 `$env:TEMP\design-refs` 로, `curl` 을 `curl.exe` 로 바꾼다.

아래 순서대로 시도하고, 앞 단계가 성공하면 멈춘다. 받은 파일이 비어 있거나 DESIGN.md 내용이 아니면(HTML 오류 페이지 등) 실패로 보고 다음 단계로 넘어간다.

```bash
mkdir -p /tmp/design-refs
# 1순위: npm 패키지 (86개 전부 포함)
npx -y getdesign add <slug> --out /tmp/design-refs/<slug>.md --force
# 2순위: 원본 GitHub 저장소 (discord, mobbin 제외 84개)
curl -fsSL https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<slug>/DESIGN.md -o /tmp/design-refs/<slug>.md
# 3순위: 내 GitHub 포크 (원본이 사라졌을 때 대비, discord·mobbin 제외)
curl -fsSL https://raw.githubusercontent.com/deserite/awesome-design-md/main/design-md/<slug>/DESIGN.md -o /tmp/design-refs/<slug>.md
```

- 어느 단계에서 받았는지 결과물 끝의 레퍼런스 표기에 함께 적는다. 예: "디자인 레퍼런스: notion (내 포크에서 받음)". 2·3순위로 내려갔다면 앞 단계가 막혔다는 뜻이니 사용자에게 알린다.
- 사용자가 프로젝트에 남기길 원하면 `--out ./DESIGN.md`로 프로젝트 루트에 저장하고, CLAUDE.md에 "UI 작업 전 DESIGN.md를 읽을 것" 한 줄을 제안한다.
- 둘 다 실패하면(네트워크 차단 등) 아래 색인의 모드·포인트 색과 한 줄 설명만으로 근사하게 만들고, 원본을 못 읽었다고 사용자에게 알린다.

### 3. 파일 읽는 법

- 맨 위 YAML frontmatter(`colors`, `typography`, `rounded`, `spacing` 등)가 토큰이다. 그대로 CSS 변수로 옮긴다.
- 본문은 `Overview` → `Colors` → `Typography` → `Layout` → `Elevation & Depth` → `Shapes` → `Components` → `Do's and Don'ts` → `Responsive Behavior` 순서. 일부 오래된 파일은 frontmatter 없이 `## 1. Visual Theme & Atmosphere`부터 시작하는데, 그때는 본문의 hex 값과 규칙을 직접 뽑는다.
- **Do's and Don'ts는 반드시 지킨다.** 이 섹션이 결과물 품질을 가장 많이 좌우한다.

### 4. 적용 규칙

- 토큰을 `:root` CSS 변수로 먼저 선언하고, 컴포넌트는 변수만 참조한다. 임의의 새 색을 만들지 않는다.
- 포인트 색은 파일이 허용한 자리(주요 CTA, 포커스, 링크 등)에만 쓴다. 장식용으로 퍼뜨리지 않는다.
- 다크/라이트가 둘 다 정의된 레퍼런스는 사용자가 정하지 않으면 파일의 기본 캔버스를 따른다.
- **폰트** — 아래 「폰트 가져오기」 섹션대로 레퍼런스 폰트를 찾아 실제로 불러온다. 이름만 적고 불러오지 않으면 기본 폰트로 떨어진다.
- 간격·모서리·그림자 값은 파일 수치를 그대로 쓴다.
- 결과물 끝에 사용한 레퍼런스와 폰트를 한 줄로 밝힌다. 예: "디자인 레퍼런스: linear.app (다크) · 폰트 Linear Display → Inter".

### 5. 지켜야 할 선 (중요)

레퍼런스는 **스타일(색, 타이포, 간격, 레이아웃 원칙)**만 빌린다.
- 해당 브랜드의 이름, 로고, 워드마크, 마스코트, 제품 사진, 고유 카피를 넣지 않는다.
- 그 회사의 실제 사이트·로그인·결제 화면처럼 보이게 만들지 않는다. 사용자가 요청해도 마찬가지다.
- 결과물은 사용자의 콘텐츠와 이름으로 채운다.

## 폰트 가져오기

목표는 레퍼런스의 글꼴 느낌을 실제 화면에 살리는 것이다. 폰트 이름을 CSS에 적는 것만으로는 안 되고, 반드시 **불러오는 코드**까지 넣는다.

### 원칙 (라이선스)

- 상용 폰트 파일(브랜드 사이트의 woff 등)을 내려받거나 링크하지 않는다. 라이선스 위반이다.
- 원본이 무료 오픈 라이선스 폰트면 **그 폰트를 그대로** 쓴다(Geist, Inter, IBM Plex, Roboto 등).
- 원본이 상용 폰트면 아래 표의 **비슷한 무료 폰트**(Google Fonts · 대부분 SIL OFL — 상업 사용·웹 임베드 가능)로 바꾼다.
- 사용자가 원본 폰트의 라이선스를 갖고 설치해 두었다고 하면, `local("원본 이름")` 을 맨 앞에 두고 무료 폰트를 뒤에 둔다. 파일을 복사하거나 웹에 올리지는 않는다.
- 결과물 끝 레퍼런스 표기에 폰트도 적는다. 예: "디자인 레퍼런스: stripe · 폰트 Söhne → Inter Tight(비슷한 무료 폰트)".

### 순서

1. 받은 DESIGN.md frontmatter `typography` 의 `fontFamily` 값에서 **역할별(디스플레이 · 본문 · 모노) 첫 번째 폰트 이름**을 뽑는다. frontmatter가 없으면 본문의 Typography 섹션에서 찾는다.
2. 아래 「폰트 매핑표」에서 찾는다. 대소문자, 공백·하이픈, `VF`·`Variable`·`Display`·`Text`·`Pro` 같은 꼬리는 무시하고 맞춘다.
3. 표에 없으면 DESIGN.md의 폰트 설명(geometric · grotesk · humanist · serif · mono · condensed · rounded)을 보고 「표에 없을 때」에서 고른다.
4. 쓸 폰트를 불러오는 코드를 `<head>` 에 넣는다(아래 「불러오기」).
5. `font-family` 는 **영문 폰트 → 한글 폰트 → 일반 계열** 순서로 쓴다. 영문 글자는 레퍼런스 느낌으로, 한글은 한글 폰트로 그려진다.
   ```css
   --font-display: "Inter Tight", "Pretendard Variable", "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
   --font-body:    "Inter", "Pretendard Variable", "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
   --font-mono:    "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
   ```
6. 원본의 웨이트 · 자간 · 줄간격 값은 바꾼 폰트에도 그대로 옮긴다. 단 한글 본문에 큰 음수 자간은 피한다(−0.01em까지).
7. 확인: 브라우저로 열 수 있으면 `await document.fonts.ready` 뒤 `document.fonts.check('16px "Inter Tight"')` 가 `true` 인지 본다. 못 열면 최소한 `<link>` 주소의 폰트 이름 철자와 웨이트가 표와 맞는지 다시 확인한다.

### 불러오기

**Google Fonts** — 아티팩트(외부 호스트는 Google Fonts만 허용)와 로컬 모두 쓸 수 있다.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Inter:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
```

- 폰트 이름의 공백은 `+` 로, 필요한 웨이트만 `:wght@400;600;700` 처럼 나열한다.
- 표에서 **단일 웨이트**로 표시된 폰트는 `:wght@…` 를 붙이지 않는다(붙이면 그 줄 전체가 400 오류로 안 불러와진다).
- 폰트에 없는 웨이트를 넣어도 같은 오류가 난다. 범위가 좁은 폰트는 가장 가까운 웨이트로 바꿔 넣는다: Lato(100·300·400·700·900) · Titillium Web(200·300·400·600·700·900) · DM Mono(300·400·500) · Playfair Display(400~900) · Chakra Petch · Space Grotesk(300~700) · IBM Plex Sans KR(100~700) · Manrope · Plus Jakarta Sans(200~800) · JetBrains Mono(100~800) · Open Sans(300~800).

**Pretendard** — 로컬 HTML · 사내 앱에서 한글 기본. 아티팩트에서는 막히므로 `Noto Sans KR` 만 쓴다.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css">
```
(폰트 이름: `"Pretendard Variable"`)

**한글 짝**: 산세리프 → `Pretendard Variable`(로컬) / `Noto Sans KR`(아티팩트) · 세리프 → `Noto Serif KR` · IBM Plex 계열 → `IBM Plex Sans KR` · 모노 → 한글이 거의 없으므로 산세리프 한글 짝을 뒤에 둔다.

### 맥 · 윈도우 모두에서 같게 보이게

결과물은 맥과 윈도우에서 모두 열린다고 가정한다.
- **웹폰트를 항상 불러온다.** 시스템 폰트에 기대지 않는다. `-apple-system`·SF Pro·Helvetica Neue·`ui-rounded` 는 맥에만 있으므로, 쓰더라도 바로 뒤에 불러온 무료 폰트를 둔다(윈도우는 그 폰트로 그려진다).
- 한글도 웹폰트(Pretendard 또는 Noto Sans KR)를 불러온다. 맥은 Apple SD Gothic Neo, 윈도우는 맑은 고딕으로 떨어지면 모양이 크게 달라진다. 두 OS 기본 한글 폰트는 스택 맨 끝 대비용으로만 둔다.
- 모노 스택은 `"JetBrains Mono", ui-monospace, Menlo, Consolas, monospace` — Menlo는 맥, Consolas는 윈도우 대비.
- 윈도우는 아주 가는 글씨가 흐리게 보인다. 레퍼런스가 200~300 웨이트를 써도 **본문은 400 이상**, 큰 제목만 300까지.
- `-webkit-font-smoothing: antialiased` 는 맥에만 먹는다. 넣어도 되지만 윈도우에서 같은 두께를 기대하지 않는다.

### 폰트 매핑표

관계: **같음** = 원본이 무료라 그대로 · **비슷** = 상용 원본 대신 비슷한 무료 폰트 · **시스템** = OS 기본 폰트(파일을 넣지 않음, 웹에서는 괄호 안 무료 폰트를 뒤에).

| 원본 폰트 (DESIGN.md 표기) | 쓰는 레퍼런스 | 쓸 폰트 | 관계 |
|---|---|---|---|
| Inter · Inter Display · Inter Variable | 1win, airtable, cal, clay, clickhouse, expo, framer, jobright, mintlify, mistral.ai, raycast, resend, revolut, voltagent, warp, wise, zapier | Inter | 같음 |
| Geist | vercel | Geist | 같음 |
| Geist Mono · GeistMono | vercel, mintlify, resend, x.ai | Geist Mono | 같음 |
| JetBrains Mono | cal, claude, clickhouse, mistral.ai, replicate | JetBrains Mono | 같음 |
| IBM Plex Sans (Variable) | ibm, posthog | IBM Plex Sans (+ IBM Plex Sans KR) | 같음 |
| Roboto | aljazeera | Roboto | 같음 |
| Open Sans | dji | Open Sans | 같음 |
| Titillium Web | jobright | Titillium Web | 같음 |
| DM Sans | minimax | DM Sans | 같음 |
| DM Mono | warp | DM Mono | 같음 |
| Source Code Pro | mongodb, posthog | Source Code Pro | 같음 |
| Rubik | sentry | Rubik | 같음 |
| Instrument Serif | warp | Instrument Serif · 단일 웨이트 | 같음 |
| Cal Sans | cal | Cal Sans · 단일 웨이트 | 같음 |
| sohne-var (Söhne) | stripe | Inter Tight | 비슷 |
| Linear Display · Linear Text | linear.app | Inter | 비슷 |
| Linear Mono · Berkeley Mono · SFMono · Monaco · ui-monospace | linear.app, opencode.ai, voltagent, sentry, ollama, posthog, shopify, supabase | JetBrains Mono | 비슷 |
| SF Pro Display · SF Pro Text | apple | Inter (맥에서는 앞에 `-apple-system`) | 시스템 |
| SF Pro Rounded | ollama | Nunito (맥에서는 앞에 `ui-rounded`) | 시스템 |
| Helvetica · Helvetica Neue | nike, resend, dell-1996 | Inter Tight (맥에서는 앞에 Helvetica Neue) | 시스템 |
| Arial · Arial Black · Georgia · Times New Roman | dell-1996, nintendo-2001, oracle | 그대로 (맥·윈도우 모두 기본 설치) | 시스템 |
| Haas Groot Disp · Haas · NeueHaasGrotesk · Helvetica Now | airtable, shopify, nike | Inter Tight | 비슷 |
| Unica77 · CohereText · Forma DJR · arcadia · rb-freigeist-neue · UberMove · CursorGothic · Waldenburg | cohere, hp, mercury, replicate, uber, cursor, elevenlabs, sanity | Inter Tight | 비슷 |
| figmaSans · hashicorpSans · Notion Sans · Pin Sans · Saans · AkkuratLL · basier-square · WF Visual Sans · universalSans · Universal Sans · abcDiatype · abcNormal · Coinbase Display · Super Sans · Kraken · Plain · Camera Plain | figma, hashicorp, notion, pinterest, intercom, mobbin, oura, replicate, webflow, x.ai, tesla, composio, runwayml, coinbase, superhuman, kraken, clay, lovable | Inter | 비슷 |
| figmaMono · SaansMono · CohereMono · WFVisualSans-Mono · Bugatti Monospace · PP Neue Montreal Mono | figma, intercom, cohere, webflow, bugatti, together.ai | DM Mono | 비슷 |
| Circular · Airbnb Cereal · SpotifyMixUI · SoDoSans · Optimistic VF · Averta | supabase, airbnb, spotify, starbucks, meta, mydealz | Figtree | 비슷 |
| GT Walsheim · The Future · NouvelR | framer, together.ai, renault | Outfit | 비슷 |
| Euclid Circular A | mongodb | Plus Jakarta Sans | 비슷 |
| Roobert · Aeonik · Degular · BinanceNova | miro, revolut, zapier, binance | Manrope | 비슷 |
| BinancePlex | binance | IBM Plex Sans | 비슷 (원본이 Plex 기반) |
| StyreneB | claude | DM Sans | 비슷 |
| Gotham | nerdwallet | Montserrat | 비슷 |
| MarkForMC | mastercard | Poppins | 비슷 |
| Apercu | wired | Work Sans | 비슷 |
| ABC Favorit | resend | Space Grotesk | 비슷 |
| Salesforce-Avant-Garde | slack | Questrial · 단일 웨이트 | 비슷 |
| Salesforce-Sans | slack | Lato | 비슷 |
| PlayStation SST · Oracle Sans | playstation, oracle | Source Sans 3 | 비슷 |
| 72 Brand | sap | Noto Sans | 비슷 |
| D-DIN · NVIDIA-EMEA · BMW Type Next · FerrariSans | spacex, nvidia, bmw, bmw-m, ferrari | Barlow | 비슷 |
| LamboType | lamborghini | Chakra Petch | 비슷 |
| Bugatti Display | bugatti | Michroma · 단일 웨이트 | 비슷 |
| Bugatti Text | bugatti | Montserrat | 비슷 |
| Sentri Display | sentry | Rubik | 비슷 |
| Vodafone | vodafone | Rubik | 비슷 |
| Nike Futura ND · Manuka | nike, theverge | Anton · 단일 웨이트 | 비슷 |
| Wise Sans | wise | Archivo Black · 단일 웨이트 | 비슷 |
| ABC Ginto Nord | discord | Unbounded | 비슷 |
| Copernicus · Tiempos | claude | Source Serif 4 | 비슷 |
| BreveText | wired | Source Serif 4 | 비슷 |
| PP Editorial Old · Editorial New | mistral.ai, oura | Instrument Serif · 단일 웨이트 | 비슷 |
| Domaine Display · WiredDisplay | resend, wired | Playfair Display | 비슷 |

### 표에 없을 때

| 원본 설명 | 쓸 폰트 |
|---|---|
| 중립 그로테스크 · 네오 그로테스크 (Helvetica 계열) | Inter Tight |
| 일반 UI 산세리프 | Inter |
| 기하학적 (Futura · Circular 계열) | Figtree · 더 둥글면 Outfit |
| 휴머니스트 | Source Sans 3 |
| 각지고 기술적 (DIN 계열) | Barlow |
| 넓은 디스플레이 | Unbounded · 아주 넓으면 Michroma |
| 좁고 굵은 디스플레이 | Anton |
| 둥근 | Nunito |
| 본문 세리프 | Source Serif 4 |
| 디스플레이 세리프 | Playfair Display · 가늘고 우아하면 Instrument Serif |
| 모노 | JetBrains Mono · 부드러우면 DM Mono |

## 용도별 추천 (참고용 출발점)

자주 쓰는 용도의 기본 후보다. 실제 추천은 위 1단계 기준대로 전체 색인에서 고른다.

| 용도 | 1순위 | 대안 |
|---|---|---|
| 관리 도구·어드민 | vercel | linear.app(다크), supabase, cal |
| 모니터링·운영 대시보드 | linear.app | sentry(다크), posthog, ibm |
| 보고서·문서형 페이지 | notion | ibm, sap, wired |
| 보고·발표형 랜딩 | stripe | apple, cohere |
| 데이터 표가 많은 화면 | ibm | airtable, sap, mydealz |
| 따뜻하고 부드러운 톤 | claude | intercom, oura, lovable, cursor |
| 개발자·터미널 감성 | opencode.ai | warp, voltagent, ollama |
| 아주 미니멀하게 | ollama | mobbin, vercel, x.ai |

## 내 디자인

사용자가 직접 만든 DESIGN.md를 여기에 등록한다. 카탈로그보다 우선한다.
(아직 등록된 것 없음. 추가하려면 "design-kit에 내 디자인 추가해줘"라고 요청하면 이 섹션을 업데이트한다.)

## 전체 색인 (86개)

형식: `slug` — 모드(L 라이트 / D 다크 / L·D 혼합) · 포인트 색 · 특징

### 개발자 도구·인프라
- `vercel` — L · #171717 · 흑백 정밀, Geist 폰트, 군더더기 없는 개발자 플랫폼
- `linear.app` — D · #5e6ad2 · 초미니멀 다크, 라벤더 포인트 하나, 촘촘한 제품 UI
- `cal` — L · #111111 · 깔끔한 중립 UI, 검정 CTA, 개발자 친화
- `supabase` — L·D · #3ecf8e · 흑백 + 에메랄드 CTA, 코드 중심
- `sentry` — D · #150f23 · 보라 미드나이트 + 라임, 데이터 밀도 높은 대시보드
- `posthog` — L · #f7a501 · 크림 바탕, 장난스러운 개발자 툴
- `clickhouse` — D · #faff69 · 검정 + 전기 노랑, 기술 문서형
- `composio` — D · #0007cd · 다크 + 딥 일렉트릭 블루
- `cursor` — L · #f54e00 · 따뜻한 크림 에디토리얼 + 오렌지
- `expo` — L · #000000 · 흰 바탕, 좁은 자간, 코드 중심
- `framer` — D · #ffffff · 검정 아트보드, 모션 중심
- `hashicorp` — D · 흑백 · 엔터프라이즈 다크, 제품별 포인트 색
- `mintlify` — L · #0a0a0a · 읽기 최적화 문서, 하늘 그라데이션 히어로
- `mongodb` — L·D · #00ed64 · 딥 틸 밴드 + 형광 그린
- `ollama` — L · #000000 · README 같은 극미니멀
- `opencode.ai` — L · #201d1d · 전부 모노스페이스, 터미널 감성
- `raycast` — D · #ffffff · 제품 스크린샷 같은 다크 크롬
- `replicate` — L · #ea2804 · 크림 + 핫 오렌지, 코드 중심
- `resend` — D · #fcfdff · 검정 + 세리프 디스플레이, 모노 포인트
- `sanity` — D · #f36458 · 거의 검정 캔버스, 강한 음수 자간, 선명한 포인트
- `voltagent` — D · #00d992 · 보이드 블랙 + 에메랄드, 터미널 네이티브
- `warp` — D · #f7f5f0 · 따뜻한 차콜, IDE 같은 블록 UI
- `webflow` — L · #080808 · 블루 포인트의 폴리시드 마케팅
- `together.ai` — L·D · #000000 · 블루프린트 스타일 기술 인프라

### AI 플랫폼
- `claude` — L · #cc785c · 크림 캔버스, 세리프 헤드라인, 테라코타 포인트
- `cohere` — L · #17171c · 흰 에디토리얼 + 딥 그린블랙 밴드
- `elevenlabs` — L · #292524 · 잡지 같은 에디토리얼, 파스텔 분위기
- `lovable` — L · #1c1c1c · 양피지 크림, 투명도로 만든 회색 체계
- `minimax` — L · #0a0a0a · 흰 캔버스 + 검정 필 버튼
- `mistral.ai` — L · #fa520f · 노을 그라데이션, 세리프 디스플레이
- `runwayml` — D · 쿨 그레이 · 시네마틱, 사진·영상이 곧 UI
- `x.ai` — D · #ffffff · 극단적 모노크롬, 미래지향
- `nvidia` — L·D · #76b900 · 그린 + 블랙, 엔지니어링 파워

### 생산성·협업
- `notion` — L · #5645d4 · 따뜻한 미니멀, 일러스트, 부드러운 면
- `airtable` — L · #181d26 · 차분한 에디토리얼, 구조화된 데이터
- `figma` — L · #000000 · 흑백 프레임 + 큼직한 파스텔 블록
- `intercom` — L · #111111 · 크림 바탕, 대화형 UI 패턴
- `miro` — L · 카나리아 옐로 · 무한 캔버스, 경쾌함
- `slack` — L · #4a154b · 딥 오버진 + 필 CTA
- `superhuman` — L·D · #1b1938 · 프리미엄 다크 히어로, 보라 글로우
- `zapier` — L · #ff4f00 · 따뜻한 크림 + 오렌지, 일러스트
- `discord` — D · #5865f2 · 딥 인디고 + 블러플, 굵은 대문자 (npm 전용)
- `mobbin` — L · #0066ff · 갤러리 화이트 모노크롬, 콘텐츠가 주인공 (npm 전용)
- `jobright` — L · #00f0a0 · 민트 그린 + 검정 필 버튼
- `clay` — L · #0a0a0a · 클레이 일러스트 + 데이터, 부드러운 그라데이션

### 핀테크·크립토
- `stripe` — L · #533afd · 딥 네이비 + 인디고, 얇은 웨이트의 우아함, 그라데이션
- `coinbase` — L · #0052ff · 신뢰감 있는 블루, 기관형
- `mercury` — L·D · #5266eb · 잉크 바이올렛 밤 + 인디고 필
- `revolut` — D · #494fdf · 검정 + 코발트 바이올렛, 그라데이션 카드
- `wise` — L · #9fe870 · 라임 그린 + 두꺼운 검정 디스플레이
- `kraken` — L · #7132f5 · 보라 포인트, 신뢰감 있는 거래소
- `binance` — D · #fcd535 · 검정 + 노랑, 트레이딩 플로어 긴장감
- `1win` — D · #00b24b · 검정 + 그린 액션, 고밀도
- `mastercard` — L · #f79e1b · 퍼티 크림, 둥근 궤도형 필, 에디토리얼
- `nerdwallet` — L · #008254 · 스프루스 그린 + 민트 워시

### 엔터프라이즈
- `ibm` — L · #0f62fe · Carbon 디자인 시스템, 구조적 블루, Plex 폰트
- `sap` — L · #0057d2 · 흰 캔버스 + 플랫 블루 밴드, 회색 두 단계
- `oracle` — L · #312d2a · 따뜻한 회색 사다리, 차콜 버튼만
- `hp` — L · #024ad8 · 흰 바탕 + 일렉트릭 블루, 각진 쉐브론

### 커머스·소비자
- `apple` — L · #0066cc · 넉넉한 여백, 갤러리 같은 제품 타일
- `airbnb` — L · #ff385c · 따뜻한 코랄, 사진 중심, 둥근 UI
- `nike` — L · #111111 · 모노크롬, 거대한 대문자, 전면 사진
- `pinterest` — L · #e60023 · 메이슨리 그리드, 이미지 우선
- `spotify` — D · #1ed760 · 콘텐츠 우선 다크, 필·원형 버튼
- `starbucks` — L · #00754a · 4단계 그린, 웜 크림, 풀 필 버튼
- `uber` — L · #000000 · 흑백 듀엣, 좁은 타이포, 도시 에너지
- `shopify` — D · 네온 그린 · 시네마틱 다크, 아주 얇은 타이포
- `meta` — L · #0064e0 · 사진 중심, 명암 이분할 면
- `dji` — L · #0070d5 · 스튜디오 제품 타일, 블루 필
- `playstation` — L·D · #0070d1 · 흑·백·블루 3면 챕터
- `oura` — L · #2a72de · 따뜻한 종이 크림 + 에디토리얼 세리프, 웰니스
- `mydealz` — L · #30a83c · 촘촘한 카드 피드, 고밀도 커뮤니티
- `vodafone` — L · #e60000 · 거대한 대문자 + 레드 챕터 밴드

### 자동차·하이엔드
- `tesla` — L · #3e6ae1 · 극단적 덜어내기, 전면 사진, UI 장식 없음
- `bmw` — L · #1c69d4 · 절제된 기업형 자동차
- `bmw-m` — D · #ffffff · 검정 + M 삼색 스트라이프, 대문자
- `bugatti` — D · #ffffff · 시네마 블랙, 모노크롬, 기념비적 타이포
- `ferrari` — D · #da291c · 명암 대비 에디토리얼 + 레드
- `lamborghini` — D · #ffc000 · 순수 검정 + 골드, 대문자
- `renault` — L · #ffed00 · 오로라 그라데이션, 대담한 에너지
- `spacex` — D · #000000 · 흑백, 전면 이미지, 미래지향

### 미디어·에디토리얼
- `wired` — L · #000000 · 신문 같은 밀도, 세리프 디스플레이, 모노 키커
- `theverge` — D · #3cffd0 · 애시드 민트 + 울트라바이올렛, 레이브 전단 타일
- `aljazeera` — L · #fa9000 · 촘촘한 뉴스 헤드라인, 오렌지 서명색

### 레트로
- `dell-1996` — L · #e91d2a · 90년대 카탈로그 웹, 검정 프레임, 컬러 블록
- `nintendo-2001` — L · #e60012 · Y2K 메탈 패널, 콘솔 크롬
