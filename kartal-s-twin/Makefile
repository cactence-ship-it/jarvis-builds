# Kartal S digital twin - common tasks. Run from kartal-s-twin/.
PY := .venv/bin/python

.PHONY: setup check validate inventory status test all checkpoint verify-remote
setup:          ## create/refresh the hash-locked environment (idempotent)
	bash scripts/setup_env.sh
check:          ## verify the environment without installing anything
	bash scripts/setup_env.sh --check
validate:       ## spec / registers / inventory / privacy rules
	$(PY) tools/twin.py validate
inventory:      ## regenerate COMPONENT_INVENTORY.md from assembly/vehicle_master.yaml
	$(PY) tools/twin.py inventory
status:
	$(PY) tools/twin.py status
test:           ## full unit-test suite (includes CAD export round-trips)
	$(PY) -m unittest discover -s tests -t . -v
all: setup validate test
checkpoint:     ## make checkpoint MSG="..."  -> validate, commit, push, verify
	bash scripts/checkpoint.sh "$(MSG)"
verify-remote:  ## prove local HEAD equals the GitHub branch head
	bash scripts/checkpoint.sh --verify
