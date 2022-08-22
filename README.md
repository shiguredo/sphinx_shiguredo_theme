# sphinx_shiguredo_theme

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## About Shiguredo's open source software

We will not respond to PRs or issues that have not been discussed on Discord. Also, Discord is only available in Japanese.

Please read https://github.com/shiguredo/oss/blob/master/README.en.md before use.

## 時雨堂のオープンソースソフトウェアについて

利用前に https://github.com/shiguredo/oss をお読みください。

## スクリーンショット

[![Image from Gyazo](https://i.gyazo.com/0315a144e31ba5602ac9482077fe5169.jpg)](https://gyazo.com/0315a144e31ba5602ac9482077fe5169)

## 実際に利用しているサイト

- https://sora-doc.shiguredo.jp/
- https://sora-js-sdk.shiguredo.jp/
- https://sora-ios-sdk.shiguredo.jp/
- https://sora-android-sdk.shiguredo.jp/
- https://tobi.shiguredo.app/

## デプロイ

[Cloudflare Pages](https://pages.cloudflare.com/) を利用している。

## 検索

[Meilisearch](https://www.meilisearch.com/) を利用可能。

conf.py に Meilisearch の設定を追加すると利用可能になる。

```python
html_theme_options = {
    'meilisearch': True,
    'meilisearch_api_key': 'xxx',
    'meilisearch_host_url': 'https://meilisearch.example.com/',
    'meilisearch_index_uid': 'docs'
}
```

[![Image from Gyazo](https://i.gyazo.com/79fe92ce9c8b6e8941dc747428e884a6.gif)](https://gyazo.com/79fe92ce9c8b6e8941dc747428e884a6)

## ライセンス

```
Copyright 2021-2022, Yuki Ito (Original Author)
Copyright 2021-2022, Shiguredo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
