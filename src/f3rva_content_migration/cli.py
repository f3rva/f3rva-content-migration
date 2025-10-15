import click
from .scripts.hello_world import hello_world
from .scripts.migrate_html_content import migrate_html

@click.group()
def main():
    """
    F3RVA Content Migration Tools
    """
    pass

main.add_command(hello_world)
main.add_command(migrate_html)

if __name__ == "__main__":
    main()
