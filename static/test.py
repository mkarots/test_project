

deps = {
    "func1": {"time": 10, "deps": ["func2"]},
    "func2": {"time": 20, "deps": ["func3", "func4"]},
    "func3": {"time": 30, "deps": [""]},
    "func4": {"time": 10}
}