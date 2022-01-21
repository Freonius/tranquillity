ifeq ($(OS),Windows_NT) 
RM = DEL /Q /F
CP = COPY /Y
RMDIR = RMDIR /Q /S
ifdef ComSpec
SHELL := $(ComSpec)
endif
ifdef COMSPEC
SHELL := $(COMSPEC)
endif
else
RM = rm -rf
CP = cp -f
RMDIR = rm -rf
endif


clean:
	-$(RMDIR) logs
	-$(RMDIR) data
	-$(RMDIR) build
	-$(RMDIR) coverage
	-$(RMDIR) dist
	-$(RMDIR) lint
	-$(RMDIR) .pytest_cache
	-$(RMDIR) node_modules
	-$(RM) settings.db
	-$(RM) .coverage

install:
	@echo "# TODO"

build:
	@echo "# TODO"

test:
	@echo "# TODO"

lint:
	@echo "# TODO"

publish:
	@echo "# TODO"