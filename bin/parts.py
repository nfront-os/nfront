"""bin/parts.py: nfront's parts, from paths.env and manifest.json (for
bin/status and bin/pin).

manifest.json: {"name", "parts": {part: {"path": a paths.env variable or
a path below it ("RUST_DIR/rust"), "branch", "commit"}}}.  A part is a git
repository (or a worktree of one)."""
import json, os, subprocess

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, 'manifest.json')

# the parts and where they are (a paths.env variable, then a path below it)
PARTS = [
	('tree', 'TREE'), ('tree-gcc', 'TREE_GCC'), ('tree-nix', 'TREE_NIX'),
	('tree-riscv', 'TREE_RISCV'), ('tree-upstream', 'TREE_UPSTREAM'),
	('gcc', 'GCC_DIR'),
	('rust', 'RUST_DIR'), ('rust/rust', 'RUST_DIR/rust'), ('rust/libc', 'RUST_DIR/libc'),
	('go', 'GO_DIR'), ('go/go', 'GO_DIR/go'),
	('mcp', 'MCP_DIR'),
	('plan9port', 'PLAN9PORT'),
	('dist', 'DIST'),
]

def env():
	"""paths.env's variables as absolute paths (the environment first)"""
	vals = {'DIST': HERE}
	for line in open(os.path.join(HERE, 'paths.env')):
		line = line.strip()
		if line and not line.startswith('#') and '=' in line:
			k, v = line.split('=', 1)
			vals[k] = v if v.startswith('/') else os.path.join(TOP, v)
	for k in list(vals):
		if os.environ.get(k):
			vals[k] = os.environ[k]
	return vals

def where(spec, vals=None):
	vals = vals or env()
	var, _, rest = spec.partition('/')
	return os.path.join(vals[var], rest) if rest else vals[var]

def git(d, *args):
	# a source archive made a repository keeps its git data beside it (toolchain/rust:
	# rust.git for rust/, core.worktree=../rust): Rust's bootstrap wants no rust/.git
	gd = d.rstrip('/') + '.git'
	if not os.path.exists(os.path.join(d, '.git')) and os.path.isdir(gd):
		cmd = ['git', '--git-dir=' + gd]
	else:
		cmd = ['git', '-C', d]
	r = subprocess.run(cmd + list(args), capture_output=True, text=True, cwd=d if os.path.isdir(d) else None)
	return r.stdout.strip() if r.returncode == 0 else None

# the tree's other branches: worktrees only when one works on them (dist/bin/repos
# --worktrees); without its worktree a branch is the tree repository's ref
BRANCHES = {'tree-gcc': 'gcc', 'tree-nix': 'nix', 'tree-riscv': 'riscv', 'tree-upstream': 'upstream'}

def state(d, name=None, vals=None):
	"""branch, commit, number of changed tracked files, the directory and revision to ask
	git about (gitdir, head); None if no repository there. A branch of the tree without its
	worktree (name in BRANCHES): its ref in the tree's repository, 'worktree': False"""
	if not os.path.isdir(d) or git(d, 'rev-parse', '--git-dir') is None:
		if name in BRANCHES:
			tree = where('TREE', vals)
			b = BRANCHES[name]
			commit = git(tree, 'rev-parse', '--verify', '-q', 'refs/heads/' + b) if os.path.isdir(tree) else None
			if commit:
				return {'branch': b, 'commit': commit, 'dirty': 0, 'gitdir': tree, 'head': b, 'worktree': False}
		return None
	commit = git(d, 'rev-parse', 'HEAD')
	branch = git(d, 'rev-parse', '--abbrev-ref', 'HEAD')
	dirty = git(d, 'status', '--porcelain', '--untracked-files=no') or ''
	return {'branch': branch, 'commit': commit, 'dirty': len(dirty.splitlines()), 'gitdir': d, 'head': 'HEAD', 'worktree': True}

def load():
	try:
		return json.load(open(MANIFEST))
	except OSError:
		return {'name': 'nfront', 'parts': {}}
