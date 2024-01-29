SRC_DIR = budget_app
REQ_DIR = requirements

FORCE:

prod: commit
	git push

commit: lint
	git add . && git commit -a

env: FORCE
	python3 -m venv $(SRC_DIR)/env && \
	cd $(SRC_DIR) && \
	source env/bin/activate && \
	pip3 install -r $(REQ_DIR)/requirements.txt

lint: FORCE
	source $(SRC_DIR)/env/bin/activate && \
	ruff format $(SRC_DIR) && \
	ruff check $(SRC_DIR) --fix

