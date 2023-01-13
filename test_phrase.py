class TestPhrase:
    def test_check_phrase(self):
        critical_len = 15
        phrase = input(f"Please, set a phrase shorter than {critical_len} characters: ")
        assert len(phrase) < critical_len, f"Your phrase is not shorter than {critical_len} characters"
