import click
import os

from astmatch import ASTMatchEngine


@click.command()
@click.argument('selector')
@click.argument('path', type=click.Path(exists=True), default='.')
def search(selector, path):
    path = click.format_filename(path)
    m = ASTMatchEngine()

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for fn in files:
                if fn.endswith('.py'):
                    fn = os.path.join(root, fn)
                    display_matches(m, selector, fn)
    elif path.endswith('.py'):
        display_matches(m, selector, path)


def display_matches(m, selector, filename):
    matches = list(m.match(selector, filename))
    if matches:
        with open(filename, 'rb') as f:
            for match, lineno in matches:
                f.seek(0)
                i = 1
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if i == lineno:
                        text = line.decode('utf-8')
                        output = '{}:{} {}'.format(filename, i, text)
                        click.echo(output, nl=False)
                        break
                    i += 1


if __name__ == '__main__':
    search()
