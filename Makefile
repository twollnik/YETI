.PHONY: test

test:
	python3 -m unittest tests/*/test*.py tests/test*.py -v

test_docs:
	sphinx-build -nWT -b dummy ./docs docs/_build/html

test_coverage:
	coverage run --source . --omit test*.py -m unittest tests/*/test*.py tests/test*.py

demo_copert_hot:
	python3 -m run_yeti -c example/example_configs/copert_hot_config.yaml

demo_copert_cold:
	python3 -m run_yeti -c example/example_configs/copert_cold_config.yaml

demo_hbefa_hot:
	python3 -m run_yeti -c example/example_configs/hbefa_hot_config.yaml

demo_copert_hot_fixed_speed:
	python3 -m run_yeti -c example/example_configs/copert_hot_fixed_speed_config.yaml

demo_pm_non_exhaust:
	python3 -m run_yeti -c example/example_configs/pm_non_exhaust_config.yaml

demo_hbefa_cold:
	python3 -m run_yeti -c example/example_configs/hbefa_cold_config.yaml