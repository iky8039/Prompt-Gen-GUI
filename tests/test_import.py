def test_import_version():
    import prompt_gen_gui
    assert hasattr(prompt_gen_gui, "__version__")
    assert prompt_gen_gui.__version__ == "1.3"
