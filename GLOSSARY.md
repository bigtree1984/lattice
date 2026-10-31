# 用語集

Lattice とマーケティング戦略キャンバス（MSC）の会話で使う言葉。新しい言葉が決まったらここに足す。

## キャンバスの言葉

| 用語 | 意味 | 例 |
|---|---|---|
| MSC | Marketing Strategy Canvas の略。このアプリと、その中身のキャンバスの両方を指す | |
| キャンバス | 1つの Product Category について、AIと一緒に積み上げた知識と戦略の全体。**Product Category ごとに1つ作る**。実体は1つのバンドル | エディブルコーヒーの MSC |
| Subject | Lattice でバンドル1つを指す汎用の呼び名。`subjects/<Subject>/` に置く。マーケティングでは Product Category と同じ | edible-coffee |
| Product Category | MSC を作る単位（マーケティングでの Subject）。市場分析と施策実行の単位になる。ユーザーの実務ではこれを「ブランド」と呼ぶことが多い | エディブルコーヒー |
| Brand | 商品に付く識別記号（名前・ロゴなど）。複数の Product Category にまたがって付けられる。MVV は Brand に紐づくが、便宜上各 MSC の中に置き、荷札の `brand` で束ねる | Bigtree Lab Coffee |
| Facet（ファセット） | フレームワークの箱。数が決まっていて、キャンバスの地図になる。荷札では `facet` | PEST、STP、Promotion、競合の4P |
| Facet グループ | Facet をまとめる2段の入れ子。`facets.md` に定義する | 市場環境 ＞ PEST、実行 ＞ 4P |
| facets.md | Facet の一覧とグループ構造の定義ファイル。競合の Facet の型（`competitor_template`）も持つ | |
| 競合の Facet | 議論に登った競合ごとに作る STP＋4P の5つ。L1 は「決定」ではなく「現時点での認識」 | 競合A ＞ Price |
| 層（Layer） | 情報の深さ。荷札では `layer` | L0・L1・L2・Discussion・原典 |
| L0 | 全体の目次。バンドル直下の `index.md` | |
| L1 | 決定。Facet ごとの箇条書き。Facet ごとに0か1ファイル。**自分の Facet の L2 だけから作る**。AI が真っ先に読み、人がサマリを掴むための層 | STP の決定事項 |
| L2 | 決定の文脈。理由と、選ばなかった案。**必ず1つ以上の Discussion から生まれる**。Facet の中の論点ごとに1ファイルで、Discussion ごとには分けず書き足していく | ポジショニングの考え方 |
| 原典（Source） | 渡された資料、または閲覧した記録 | 競合A 公式サイト |
| 原典カード（Source card） | 資料1つにつき1つ作る .md（`source-<名前>.md`）。荷札に何の資料かと元の場所、本文に要約とその資料についての解釈。実物があれば隣に同じ名前で置く | source-competitor-a-website.md |
| ○ 反映した | Discussion の内容が、その Facet の L2 の `sources` に入っていること | D-003 と Product |
| △ 持ち越し | 決めていないが、その Facet を決める材料がある Discussion。要約の持ち越しの行頭に Facet ID を書く | D-002 と PEST の Technology |
| 材料あり | L1 がまだ無いが、△ の付いた Discussion がある Facet | PEST の Technology |
| discussion_summary.md | 各 Discussion の要約。どのフォルダでもこの名前。会話で何を決めたか、複数の資料を読み合わせて分かったこと、原典カードへのリンク一覧 | |
| 出どころ | そのファイルがどのファイルから来たか。荷札の `sources` | L1 → L2 → Discussion → 原典 |
| Discussion（壁打ち） | ユーザーと Claude の1回の会話。`discussions/` に要約（discussion_summary.md）と資料を置く。ID は `D-001` 形式。Claude Code のセッションとは別物 | D-001 |
| 承認 | L2・L1 の変更をユーザーが OK すること。`verified: human:<呼び名>` を付け、`status` を `draft` から `stable` にする | |
| hide | L1・L2 の記述を見えなくすること。ファイルは残し、`status: deprecated` と理由（`deprecated_reason`）を書く。旧称「しまう」 | 期間が過ぎたキャンペーン案 |
| drop | L1・L2 や Discussion を削除すること。過去は git で遡る。Discussion の drop は構造のつながり（`sources`・リンク）だけを外し、L2 の文章は直さない。出どころがその Discussion だけの L2 と、その L1 は連鎖して消す。旧称「完全に消す」 | 間違っていた情報 |
| Discussion の hide・drop | Facet を hide・drop しても Discussion には手を付けない（他の Facet からも参照されうるため）。Discussion を drop するのは名指しされたときだけで、その Discussion を出どころに持つ L2 からつながりを外す（文章は直さない）。Discussion は hide しない（記録なので） | |
| old | hide したものを見る表示 | |
| FIX | 年度などの節目で L1・L2 を確定すること（git のタグ） | 2025年版の FIX |

## 外から借りている言葉

| 用語 | 意味 |
|---|---|
| OKF（Open Knowledge Format） | Google Cloud が公開した、Markdown のフォルダで知識を整理する仕様。いまは v0.2 |
| バンドル | OKF での、知識をまとめたフォルダ1つ |
| 荷札 | ファイルの頭に書く frontmatter（区切り線で挟んだ数行） |

## 使わなくなった言葉

- Topic: 一時「横断する問い」の意味で使ったが、Facet と近すぎるのでやめた。複数の Discussion にまたがる問いは Facet の未決で扱う
- Area: Facet の旧案。一般的すぎるのでやめた
- 資料のまとめ（`summary-`）: 2026-10-31 にやめた。資料1つの話は原典カードに、複数の読み合わせは discussion_summary に書く
- L3: 旧称。Discussion の要約・資料のまとめを指したが、全部 Discussion の中にあったので層としてはやめ、`layer: discussion` にした（2026-10-30）
