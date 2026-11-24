# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：  
search_materials、glossary_search_glossary
- STEP 2 の [tool call]：   
glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：   
fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：  
aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要', 'topics': ['general']})、  aws_aws___search_documentation({'topics': ['general'], 'search_phrase': '"Using versioning" "Amazon S3"'})
- 気づき・疑問：  
MCPで外部のツールをとってくることができるのは便利ですが、そもそもどんなツールが外部にあるか分からない初心者はどう調べたらよいのでしょうか。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：<br> 
*app/mcp_server.py* の# TODOの次の行に *server.tool()(tools.get_lecture_summary)* を追加した。
- 結果：<br>
`uv run python -m app.mcp_agent --list-tools`実施でツールとして*glossary_get_lecture_summary*が追加になったことを確認でした。<br>
`uv run python -m app.mcp_agent --trace "第6回では何を学びますか？"`実施で次のとおり要約されました。<br>
>
1. **外部ツール**：アプリの中の関数ではなく、プロセスや機械をまたいで呼ぶ機能（Webの取得、ファイル操作、他社APIなど）。
2. **MCP（Model Context Protocol）の役割**：ツールを公開する側（MCPサーバー）と使う側（MCPクライアント）の間の共通規約。サーバーを1つ作れば、対応するどのクライアントからも同じ手順で利用可能。
3. **サーバーが公開するもの**：ツールの名前・説明文・引数のスキーマ。モデルはこれらを読んで呼び出しを決定する。
4. **トランスポート**：プロセス間で標準入出力を使う「stdio」や、URLで待ち受ける「Streamable HTTP」といった接続方式。
5. **既製のサーバー活用と安全性**：ファイル操作やWeb取得などの既製サーバーを設定ファイルに書き足して使う方法や、勝手なコード実行を防ぐためのセキュリティ上の注意点。
- 気づき・疑問：<br>
毎回の講習でアンケート回答する際に学んだことを聞かれた際にこの要約ツールが使えそうです。
