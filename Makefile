lint:
	@if [ "$(app)" = "" ]; then \
		pylint ./apps/*/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	else \
		pylint ./apps/$(app)/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	fi

code-checker:
	@if [ "$(app)" = "" ]; then \
		flake8 apps/$(app) --exclude .git,__pycache__,"apps/*/migrations/" --max-line-length 95 --ignore=E128,E124;\
	else \
		flake8 apps/*/*.py --exclude .git,__pycache__,"apps/*/migrations/" --max-line-length 95 --ignore=E128,E124;\
	fi