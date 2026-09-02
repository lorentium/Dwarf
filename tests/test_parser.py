from dwarf.parser import has_github_agentic_workflows

def test_gh_aw_valid_pair():
    assert has_github_agentic_workflows(["report.md", "report.lock.yml"]) is True

def test_gh_aw_only_md():
    assert has_github_agentic_workflows(["report.md"]) is False

def test_gh_aw_only_lock():
    assert has_github_agentic_workflows(["report.lock.yml"]) is False

def test_gh_aw_mismatched_names():
    assert has_github_agentic_workflows(["report.md", "other.lock.yml"]) is False

def test_gh_aw_multiple_files_with_match():
    assert has_github_agentic_workflows(["README.md", "daily.md", "daily.lock.yml", "config.yml"]) is True