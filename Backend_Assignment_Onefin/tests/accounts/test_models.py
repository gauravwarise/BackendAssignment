class TestAuthUserModel:
    def test_str_method(self, authuser_factory):
        x = authuser_factory() 

        assert x.__str__() == "test_authuser"