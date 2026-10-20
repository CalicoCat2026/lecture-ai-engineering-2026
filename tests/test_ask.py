from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **_: response)
    )
    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 入力: 12, 出力: 34\n"


def test_ask_reports_missing_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **_: response)
    )
    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 入力: 不明, 出力: 不明\n"


def test_ask_uses_chat_for_follow_up_question(capsys):
    response = SimpleNamespace(
        text="文脈を踏まえた回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=20,
            candidates_token_count=15,
        ),
    )

    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return response

    chat = FakeChat()

    assert ask_module.ask("それはなぜ？", chat) == "文脈を踏まえた回答"
    assert chat.questions == ["それはなぜ？"]
    assert capsys.readouterr().out == "[トークン数] 入力: 20, 出力: 15\n"


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return SimpleNamespace(
                text=f"回答: {question}",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=1,
                    candidates_token_count=2,
                ),
            )

    chat = FakeChat()
    client = SimpleNamespace(chats=SimpleNamespace(create=lambda **_: chat))
    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    questions = iter(["続けて質問", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    ask_module.main()

    assert chat.questions == ["最初の質問", "続けて質問"]
    output = capsys.readouterr().out
    assert "回答: 最初の質問" in output
    assert "回答: 続けて質問" in output
