

# because of the relative imports, use module format rather than executing
# `python -m <pkg.module.submodule>`
# the script directly

tasks = {
    'testtask': 'python -m app.tasks.testtask.submit',
}
