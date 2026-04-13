"""
Tests for scan_owasp — OWASP Top 10 vulnerability scanner.

Static AST rules tested directly. Full scan_owasp tested with mocked Milvus.
"""

import ast
import textwrap
import pytest
from unittest.mock import patch


# ── Static Rule Detection ───────────────────────────────────────────────


class TestSQLInjection:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_sql_injection
        tree = ast.parse(textwrap.dedent(code))
        return _detect_sql_injection(tree)

    def test_fstring_sql(self):
        result = self._detect('''
            name = "test"
            query = f"SELECT * FROM users WHERE name = {name}"
        ''')
        assert result is not None
        assert "f-string" in result

    def test_concatenation_sql(self):
        result = self._detect('''
            query = "SELECT * FROM users WHERE name = " + user_input
        ''')
        assert result is not None
        assert "concatenation" in result

    def test_format_sql(self):
        result = self._detect('''
            query = "SELECT * FROM users WHERE id = {}".format(user_id)
        ''')
        assert result is not None
        assert ".format()" in result

    def test_safe_parameterized_query(self):
        result = self._detect('''
            cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        ''')
        assert result is None

    def test_safe_string_no_sql(self):
        result = self._detect('''
            msg = f"Hello {name}, welcome!"
        ''')
        assert result is None


class TestCommandInjection:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_command_injection
        tree = ast.parse(textwrap.dedent(code))
        return _detect_command_injection(tree)

    def test_os_system(self):
        result = self._detect('''
            import os
            os.system("ls -la")
        ''')
        assert result is not None
        assert "os.system" in result

    def test_subprocess_shell_true(self):
        result = self._detect('''
            import subprocess
            subprocess.run(cmd, shell=True)
        ''')
        assert result is not None
        assert "shell=True" in result

    def test_subprocess_shell_false(self):
        result = self._detect('''
            import subprocess
            subprocess.run(["ls", "-la"], shell=False)
        ''')
        assert result is None

    def test_subprocess_no_shell(self):
        result = self._detect('''
            import subprocess
            subprocess.run(["ls", "-la"])
        ''')
        assert result is None


class TestPathTraversal:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_path_traversal
        tree = ast.parse(textwrap.dedent(code))
        return _detect_path_traversal(tree)

    def test_fstring_in_open(self):
        result = self._detect('''
            f = open(f"/data/{user_input}/file.txt")
        ''')
        assert result is not None
        assert "f-string" in result

    def test_concatenation_in_path(self):
        result = self._detect('''
            p = Path("/data/" + user_input)
        ''')
        assert result is not None
        assert "concatenation" in result

    def test_safe_literal_path(self):
        result = self._detect('''
            f = open("/data/config.json")
        ''')
        assert result is None


class TestHardcodedSecrets:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_hardcoded_secrets
        tree = ast.parse(textwrap.dedent(code))
        return _detect_hardcoded_secrets(tree)

    def test_hardcoded_password(self):
        result = self._detect('''
            db_password = "super_secret_123"
        ''')
        assert result is not None
        assert "db_password" in result

    def test_hardcoded_api_key(self):
        result = self._detect('''
            api_key = "sk-abc123def456"
        ''')
        assert result is not None

    def test_env_var_password(self):
        result = self._detect('''
            password = os.getenv("DB_PASSWORD")
        ''')
        assert result is None

    def test_short_placeholder(self):
        result = self._detect('''
            api_key = "TODO"
        ''')
        assert result is None

    def test_empty_string(self):
        result = self._detect('''
            secret = ""
        ''')
        assert result is None


class TestWeakHashing:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_weak_hashing
        tree = ast.parse(textwrap.dedent(code))
        return _detect_weak_hashing(tree)

    def test_md5(self):
        result = self._detect('''
            h = hashlib.md5(data)
        ''')
        assert result is not None
        assert "md5" in result.lower()

    def test_sha1(self):
        result = self._detect('''
            h = hashlib.sha1(data)
        ''')
        assert result is not None
        assert "sha1" in result.lower()

    def test_sha256_safe(self):
        result = self._detect('''
            h = hashlib.sha256(data)
        ''')
        assert result is None

    def test_hashlib_new_md5(self):
        result = self._detect('''
            h = hashlib.new("md5", data)
        ''')
        assert result is not None


class TestUnsafeDeserialization:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_unsafe_deserialization
        tree = ast.parse(textwrap.dedent(code))
        return _detect_unsafe_deserialization(tree)

    def test_pickle_load(self):
        result = self._detect('''
            data = pickle.load(f)
        ''')
        assert result is not None
        assert "pickle" in result

    def test_pickle_loads(self):
        result = self._detect('''
            data = pickle.loads(raw)
        ''')
        assert result is not None

    def test_yaml_load_unsafe(self):
        result = self._detect('''
            data = yaml.load(stream)
        ''')
        assert result is not None
        assert "SafeLoader" in result

    def test_yaml_load_safe(self):
        result = self._detect('''
            data = yaml.load(stream, Loader=yaml.SafeLoader)
        ''')
        assert result is None

    def test_yaml_safe_load(self):
        result = self._detect('''
            data = yaml.safe_load(stream)
        ''')
        assert result is None


class TestDebugMode:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_debug_mode
        tree = ast.parse(textwrap.dedent(code))
        return _detect_debug_mode(tree)

    def test_flask_debug(self):
        result = self._detect('''
            app.run(debug=True)
        ''')
        assert result is not None
        assert "debug=True" in result

    def test_uvicorn_debug(self):
        result = self._detect('''
            uvicorn.run(app, debug=True)
        ''')
        assert result is not None

    def test_no_debug(self):
        result = self._detect('''
            app.run(host="0.0.0.0")
        ''')
        assert result is None


class TestSensitiveLogging:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_sensitive_logging
        tree = ast.parse(textwrap.dedent(code))
        return _detect_sensitive_logging(tree)

    def test_logging_password(self):
        result = self._detect('''
            log.info("User password: %s", password)
        ''')
        assert result is not None
        assert "password" in result

    def test_logging_safe(self):
        result = self._detect('''
            log.info("User %s logged in", username)
        ''')
        assert result is None


class TestEvalExec:
    def _detect(self, code):
        from backends.code_improvement_backend import _detect_eval_exec
        tree = ast.parse(textwrap.dedent(code))
        return _detect_eval_exec(tree)

    def test_eval(self):
        result = self._detect('''
            result = eval(user_input)
        ''')
        assert result is not None
        assert "eval" in result

    def test_exec(self):
        result = self._detect('''
            exec(code_string)
        ''')
        assert result is not None
        assert "exec" in result

    def test_ast_literal_eval_safe(self):
        result = self._detect('''
            result = ast.literal_eval(data)
        ''')
        assert result is None


# ── _run_static_rules ───────────────────────────────────────────────────


class TestRunStaticRules:
    def _run(self, code):
        from backends.code_improvement_backend import _run_static_rules
        return _run_static_rules(textwrap.dedent(code), "test.py")

    def test_clean_code(self):
        findings = self._run('''
            def safe_function(name: str) -> str:
                return f"Hello {name}"
        ''')
        assert len(findings) == 0

    def test_multiple_findings(self):
        findings = self._run('''
            def bad_function():
                db_password = "hardcoded123"
                query = f"SELECT * FROM users WHERE id = {user_id}"
                os.system("rm -rf /")
        ''')
        assert len(findings) >= 3
        categories = {f["category"] for f in findings}
        assert "Injection" in categories

    def test_syntax_error_handled(self):
        from backends.code_improvement_backend import _run_static_rules
        findings = _run_static_rules("def broken(:", "test.py")
        assert len(findings) == 1
        assert findings[0]["category"] == "Parse Error"

    def test_findings_have_required_fields(self):
        findings = self._run('''
            def insecure():
                h = hashlib.md5(data)
        ''')
        for f in findings:
            assert "owasp_id" in f
            assert "category" in f
            assert "severity" in f
            assert "location" in f
            assert "detail" in f

    def test_severity_levels(self):
        findings = self._run('''
            def insecure():
                query = f"SELECT * FROM users WHERE id = {uid}"
                h = hashlib.md5(data)
                data = pickle.loads(raw)
                result = eval(expr)
        ''')
        severities = {f["severity"] for f in findings}
        assert "CRITICAL" in severities  # SQL injection
        assert "HIGH" in severities      # weak hashing


# ── OWASP_RULES registry ───────────────────────────────────────────────


class TestOwaspRules:
    def test_rules_registered(self):
        from backends.code_improvement_backend import _OWASP_RULES
        assert len(_OWASP_RULES) >= 9

    def test_rules_have_required_fields(self):
        from backends.code_improvement_backend import _OWASP_RULES
        for rule in _OWASP_RULES:
            assert "owasp_id" in rule
            assert "category" in rule
            assert "severity" in rule
            assert "description" in rule
            assert "detector" in rule
            assert callable(rule["detector"])

    def test_valid_severities(self):
        from backends.code_improvement_backend import _OWASP_RULES
        valid = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
        for rule in _OWASP_RULES:
            assert rule["severity"] in valid, f"Invalid severity: {rule['severity']}"

    def test_valid_owasp_ids(self):
        from backends.code_improvement_backend import _OWASP_RULES
        for rule in _OWASP_RULES:
            assert rule["owasp_id"].startswith("A"), f"Invalid OWASP ID: {rule['owasp_id']}"


# ── scan_owasp (full function with mocked Milvus) ──────────────────────


class TestScanOwasp:
    @pytest.fixture(autouse=True)
    def mock_milvus(self):
        with patch("backends.code_improvement_backend._embed", return_value=[0.0] * 1536), \
             patch("backends.code_improvement_backend._embed_batch", return_value=[[0.0] * 1536]), \
             patch("backends.code_improvement_backend._search_by_vector", return_value=[]):
            yield

    def test_file_not_found(self):
        from backends.code_improvement_backend import scan_owasp
        result = scan_owasp("/nonexistent/file.py")
        assert "error" in result

    def test_clean_file(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "clean.py"
        f.write_text('def hello(name: str) -> str:\n    return f"Hello {name}"\n')
        result = scan_owasp(str(f))
        assert result["summary"]["risk_level"] == "CLEAN"
        assert result["summary"]["total_findings"] == 0

    def test_insecure_file(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "insecure.py"
        f.write_text(textwrap.dedent('''\
            def bad():
                query = f"SELECT * FROM users WHERE id = {uid}"
                os.system("rm -rf /")
        '''))
        result = scan_owasp(str(f))
        assert result["summary"]["risk_level"] == "CRITICAL"
        assert result["summary"]["total_findings"] >= 2
        assert len(result["static_findings"]) >= 2

    def test_returns_required_keys(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "test.py"
        f.write_text("def foo(): pass\n")
        result = scan_owasp(str(f))
        assert "file" in result
        assert "static_findings" in result
        assert "behavioral_findings" in result
        assert "summary" in result
        assert "total_findings" in result["summary"]
        assert "by_severity" in result["summary"]
        assert "by_category" in result["summary"]
        assert "risk_level" in result["summary"]

    def test_severity_counts(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "mixed.py"
        f.write_text(textwrap.dedent('''\
            def insecure():
                query = f"SELECT * FROM users WHERE id = {uid}"
                h = hashlib.md5(data)
                result = eval(expr)
        '''))
        result = scan_owasp(str(f))
        sev = result["summary"]["by_severity"]
        assert sev["CRITICAL"] >= 1  # SQL injection
        assert sev["HIGH"] >= 1      # weak hashing
        assert sev["LOW"] >= 1       # eval

    def test_behavioral_findings_with_security_hits(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "sec.py"
        f.write_text("def authenticate(user, password): pass\n")
        hit = {"score": 0.8, "name": "OWASP Top 10", "vault": "thesis",
               "summary": "OWASP security framework for web application vulnerabilities"}
        with patch("backends.code_improvement_backend._search_by_vector", return_value=[hit]):
            result = scan_owasp(str(f))
            assert len(result["behavioral_findings"]) >= 1

    def test_behavioral_findings_filter_non_security(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "normal.py"
        f.write_text("def add(a, b): return a + b\n")
        hit = {"score": 0.8, "name": "Math Utils", "vault": "test",
               "summary": "Mathematical utility functions for data processing"}
        with patch("backends.code_improvement_backend._search_by_vector", return_value=[hit]):
            result = scan_owasp(str(f))
            assert len(result["behavioral_findings"]) == 0

    def test_empty_file(self, tmp_path):
        from backends.code_improvement_backend import scan_owasp
        f = tmp_path / "empty.py"
        f.write_text("")
        result = scan_owasp(str(f))
        assert "error" in result
