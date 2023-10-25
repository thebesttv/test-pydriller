import sys
import json
from pydriller import Repository
from pygments.lexers import guess_lexer_for_filename


def guess_pl(file_name, source_code):
    """
    Guess the programming language from the source code.
    """
    try:
        return guess_lexer_for_filename(file_name, source_code).name
    except:
        return 'Unknown'


# if len(sys.argv) != 5:
#     print('Usage: python main.py <cve> <cwe> <path_to_repo> <commit_hash>')
#     exit(1)

# cve = sys.argv[1]
# cwe = sys.argv[2]
# path_to_repo = sys.argv[3]
# commit_hash = sys.argv[4]

cve = None
cwe = None
path_to_repo = 'https://github.com/jithin-renji/Nuke.git'
commit_hash = '492d7c4baa061c6fae434ddf5622501ff4d36455'


repository = Repository(
    path_to_repo=path_to_repo,
    single=commit_hash
)

result = {
    'cve': cve,
    'cwe': cwe,
    'commit': commit_hash,
    'url': path_to_repo,
    'functions': [],
}

for commit in repository.traverse_commits():
    print(commit.hash)

    for file in commit.modified_files:
        programming_language = guess_pl(file.filename, file.source_code)

        if programming_language not in ['C', 'C++']:
            continue

        print(file.new_path, programming_language)

        for method in file.methods:
            result['functions'].append({
                'name': method.name,
                'path': file.new_path,
                'start_line': method.start_line,
                'end_line': method.end_line,
            })
            print(f' {method.start_line} {method.end_line}')

    for parent in commit.parents:
        print('> ' + parent)


with open(f'{commit_hash}.json', 'w') as f:
    json.dump(result, f, indent=4, sort_keys=False)
