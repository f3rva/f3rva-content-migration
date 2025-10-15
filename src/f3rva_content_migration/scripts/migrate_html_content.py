import click
import mysql.connector
import requests
import time
import os

@click.command("migrate-html")
@click.option('--db-host', default='localhost', help='Database host.')
@click.option('--db-user', required=True, help='Database user.')
@click.option('--db-password', required=True, help='Database password.')
@click.option('--db-name', required=True, help='Database name.')
@click.option('--wp-host', required=True, help='WordPress host.')
def migrate_html(db_host, db_user, db_password, db_name, wp_host):
    """
    Migrates missing author and HTML content from a WordPress API to the database.
    """
    click.echo("Starting migration of HTML content...")

    try:
        # Connect to the database
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor(dictionary=True)

        # Step 1: Query for records with missing information
        click.echo("Step 1: Querying for records with missing author or HTML content...")
        query = """
            SELECT w.WORKOUT_ID, w.TITLE, w.SLUG, w.WORKOUT_DATE, w.BACKBLAST_URL
            FROM WORKOUT w
            LEFT JOIN WORKOUT_DETAILS wd ON w.WORKOUT_ID = wd.WORKOUT_ID
            WHERE w.AUTHOR IS NULL OR wd.HTML_CONTENT IS NULL OR wd.HTML_CONTENT = ''
        """
        cursor.execute(query)
        records_to_process = cursor.fetchall()
        click.echo(f"Found {len(records_to_process)} records to process.")

        # Offline storage for records not found or with errors
        error_records = []
        not_found_records = []

        # Step 2: Call WordPress API for each record
        click.echo("Step 2: Fetching data from WordPress API...")
        for record in records_to_process:
            workout_id = record['WORKOUT_ID']
            slug = record['SLUG']
            workout_date = record['WORKOUT_DATE'].strftime('%Y-%m-%d')
            
            if not slug or not workout_date:
                click.echo(f"Skipping WORKOUT_ID {workout_id} due to missing slug or workout_date.")
                continue

            api_url = f"{wp_host}/wp-json/f3-data/v1/workout-slug-date/{slug}/{workout_date}"
            
            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                if response.status_code == 200:
                    data = response.json()
                    if data and data.get('author_name') and data.get('html_content'):
                        # Step 3: Update database
                        update_author(cursor, workout_id, data['author_name'])
                        insert_html_content(cursor, workout_id, data['html_content'])
                        db_connection.commit()
                        click.echo(f"Successfully updated WORKOUT_ID {workout_id}")
                    else:
                        not_found_records.append(record)
                        click.echo(f"No data returned from API for WORKOUT_ID {workout_id}")

                else:
                    not_found_records.append(record)
                    click.echo(f"API returned status {response.status_code} for WORKOUT_ID {workout_id}")

            except requests.exceptions.RequestException as e:
                error_records.append({'record': record, 'error': str(e)})
                click.echo(f"Error fetching data for WORKOUT_ID {workout_id}: {e}")

            # Wait between API calls
            time.sleep(5)

        # Save error/not found records
        save_offline(error_records, 'error_records.txt')
        save_offline(not_found_records, 'not_found_records.txt')

        cursor.close()
        db_connection.close()
        click.echo("Migration finished.")

    except mysql.connector.Error as err:
        click.echo(f"Database error: {err}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)

def update_author(cursor, workout_id, author_name):
    """Updates the author for a given workout."""
    update_query = "UPDATE WORKOUT SET AUTHOR = %s WHERE WORKOUT_ID = %s AND AUTHOR IS NULL"
    cursor.execute(update_query, (author_name, workout_id))

def insert_html_content(cursor, workout_id, html_content):
    """Inserts or updates HTML content for a given workout."""
    check_query = "SELECT 1 FROM WORKOUT_DETAILS WHERE WORKOUT_ID = %s"
    cursor.execute(check_query, (workout_id,))
    exists = cursor.fetchone()

    if not exists:
        insert_query = "INSERT INTO WORKOUT_DETAILS (WORKOUT_ID, HTML_CONTENT) VALUES (%s, %s)"
        cursor.execute(insert_query, (workout_id, html_content))

def save_offline(records, filename):
    """Saves records to a file for later inspection."""
    if records:
        with open(filename, 'w') as f:
            for item in records:
                f.write(f"{item}\n")
        click.echo(f"Saved {len(records)} records to {filename}")

if __name__ == '__main__':
    migrate_html()
