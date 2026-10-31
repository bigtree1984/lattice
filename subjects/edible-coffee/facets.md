---
type: Facet Definition
title: Facet 一覧
description: この MSC の Facet と、その2段のグループ構造の定義。ビューアーと Claude はここを読んで Facet を並べる。
generated:
  by: claude/opus-5-5
  at: 2026-10-30T10:40:00+09:00
groups:
  - id: market
    label: 市場環境
    groups:
      - id: pest
        label: PEST
        facets:
          - { id: pest-political, label: Political }
          - { id: pest-economic, label: Economic }
          - { id: pest-society, label: Society }
          - { id: pest-technology, label: Technology }
      - id: five-forces
        label: 5F
        facets:
          - { id: five-forces, label: 5F }
      - id: swot
        label: SWOT
        facets:
          - { id: swot, label: SWOT }
  - id: strategy
    label: 戦略
    groups:
      - id: stp
        label: STP
        facets:
          - { id: stp, label: STP }
      - id: mvv
        label: MVV
        facets:
          - { id: mvv, label: MVV }
  - id: customer
    label: 顧客
    groups:
      - id: persona
        label: ペルソナ
        facets:
          - { id: persona, label: ペルソナ }
      - id: journey
        label: カスタマージャーニー
        facets:
          - { id: journey, label: カスタマージャーニー }
  - id: execution
    label: 実行
    groups:
      - id: 4p
        label: 4P（自社）
        facets:
          - { id: product, label: Product }
          - { id: price, label: Price }
          - { id: place, label: Place }
          - { id: promotion, label: Promotion }
  - id: competition
    label: 競合
    groups:
      - id: competitor-a
        label: 競合A
        facets:
          - { id: competitor-a-stp, label: STP }
          - { id: competitor-a-product, label: Product }
          - { id: competitor-a-price, label: Price }
          - { id: competitor-a-place, label: Place }
          - { id: competitor-a-promotion, label: Promotion }
      - id: competitor-b
        label: 競合B
        facets:
          - { id: competitor-b-stp, label: STP }
          - { id: competitor-b-product, label: Product }
          - { id: competitor-b-price, label: Price }
          - { id: competitor-b-place, label: Place }
          - { id: competitor-b-promotion, label: Promotion }
competitor_template:
  - { suffix: stp, label: STP }
  - { suffix: product, label: Product }
  - { suffix: price, label: Price }
  - { suffix: place, label: Place }
  - { suffix: promotion, label: Promotion }
---

# Facet 一覧

この MSC で使う Facet の定義。構造は「グループ（大）＞ グループ（小）＞ Facet」の2段。

- Facet のフォルダは `facets/<Facet ID>/` に**平らに**置く。グループはこのファイルにだけ書く。
  - 理由: グループを組み替えても、ファイルの移動やリンクの書き換えが要らない。
- Facet ID はバンドル全体で重複させない。グループ内で分けるものは `pest-society` のようにグループ名を頭に付ける。
- 他の業務に転用するときは、このファイルを差し替える。

## 各 Facet に書くこと

### 市場環境
- **PEST**: 政治・経済・社会・技術の外部環境。Facet は4つに分ける（社内の説明が「市場環境 ― PEST ― Society」の粒度で行われるため）。
- **5F**: 新規参入・代替品・買い手・売り手・業界内競争。いまは1つの Facet。
- **SWOT**: 自社の強み・弱みと、外部の機会・脅威。いまは1つの Facet。

### 戦略
- **STP**: セグメンテーション・ターゲティング・ポジショニング。いまは1つの Facet。
- **MVV**: ミッション・ビジョン・バリュー。Brand に紐づく。荷札に `brand` を書き、同じ Brand の他の MSC と揃える。

### 顧客
- **ペルソナ**: 狙う人物像。
- **カスタマージャーニー**: 購入までと購入後の行動。

### 実行
- **4P（自社）**: Product・Price・Place・Promotion。施策の実行単位。

### 競合
- **自社の Facet は最初から枠を用意する**（議論して決めるものなので、空の箱も「まだ議論していない」という情報になる）。
- **競合の Facet は、議論に登ったときに作る。** 競合ごとに小グループを1つ作り、中に `competitor_template` の5つ（STP＋4P）を置く。ID は `competitor-<名前>-<suffix>`。
  - 外から観察できるのは STP と 4P まで。MVV・ペルソナ・カスタマージャーニーは、資料が揃った競合にだけ足す。
- 競合の L1 は「決定」ではなく「現時点での認識」。自社の決定と同じく、だいきさんの承認で `stable` にする。

## 粒度の不揃い

PEST と 4P は中の要素ごとに Facet を分け、5F・SWOT・STP・MVV は1つの Facet にしている。議論がその粒度で必要になったら、ここで分ける。
