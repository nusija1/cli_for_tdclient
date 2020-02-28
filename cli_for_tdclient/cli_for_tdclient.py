import click
import tdclient
import pandas as pd
from tabulate import tabulate

TD_API_KEY = "10574/6f3458aa29a065296977fdc5d06284fc8c6b3072"


def validate_db(ctx=None, param=None):
    with tdclient.Client(apikey=TD_API_KEY) as client:
        database_list = client.api.list_databases()
        for value in database_list.items():
            if param == value[0]:
                return param
        if param != value[0]:
            raise Exception('Check db name', ctx)


def validate_engine(ctx=None, param=None):
    if param in "presto, hive":
        return param
    else:
        raise click.BadParameter('Engine value can be presto or hive', ctx)


@click.command()
@click.option("--db_name", "-d", callback=validate_db, required=True, type=click.STRING,
              help="Please fill in name of DB you want to connect with")
@click.option("--table_name", "-t", required=True, type=click.STRING,
              help="Please fill in name of table you want to issue a query from")
@click.option("--column", "-c", required=False, type=click.STRING,
              help="Use this parameter to add list of columns you want to query. //"
                   "Please use comma as a separator if you want to see more than i collumn. //"
                   "If nothing given - all columns will be returned.")
@click.option("--engine", "-e", callback=validate_engine, default="presto")
@click.option("--min_time", "-m", required=False,
              help="minimum timestamp ​'min_time'​ in unix timestamp or ​NULL")
@click.option("--max_time", "-M", required=False,
              help="minimum timestamp ​'min_time'​ in unix timestamp or ​NULL")
@click.option("--limit", help="limit")
@click.option("--format", "-f", required=False, type=click.Choice(['csv', 'tab']), default='tab',
              help="File to store the result, will be saved in the /n"
                   " same dir as this script")
def db_connect(db_name, table_name, engine=None, column=None, min_time=None, max_time=None, limit=None, format=None):
    with tdclient.Client(apikey=TD_API_KEY) as client:
        existing_columns = []
        data = client.table(db_name, table_name)
        d = data.schema
        for i in d:
            i = i[0]
            existing_columns.append(i)
        print(existing_columns)
        if column is None:
            column = ','.join(str(e) for e in existing_columns)
            print("Your column param is ok: {}".format(column))
        elif "," in column:
            column = column.split(",")
            set(column).issubset(existing_columns)
            column = ','.join(column)
            print("Your column param is ok: {}".format(column))
        elif "*" in column:
            column = ','.join(str(e) for e in existing_columns)
            print("Your column param is ok: {}".format(column))
        else:
            raise Exception(
                'Check your column param send correct name for column. This is correct list {} and this is what you have: {}'.format(
                    existing_columns, column))
        if min_time is None or min_time > max_time:
            min_time = 'NULL'
            print(
                'You set up min_time < max_time or None. We changed your min_time to NULL so you can get more correct data')
        else:
            min_time = min_time
            print('Your min_time =' + min_time)
        if max_time is None or max_time < min_time:
            max_time = 'NULL'
            print(
                'You set up max_time < min_time or None. We changed your max_time to NULL so you can get more correct data')
        else:
            max_time = max_time
            print('Your max_time =' + max_time)
        if limit is not None:
            job = client.query(db_name,
                               "SELECT {} FROM {} where TD_TIME_RANGE(time, {}, {}) limit {}".format(
                                   column, table_name,
                                   min_time, max_time,
                                   limit), type=engine)
        else:
            job = client.query(db_name,
                               "SELECT {} FROM {} where TD_TIME_RANGE(time, {}, {})".format(
                                   column, table_name,
                                   min_time, max_time), type=engine)
            # sleep until job's finish
        job.wait()
        if job.num_records == 0:
            print("Your query returned 0 rows")
        f = open('output.' + format, "+w")
        with f:
            if format == 'csv':
                f.write(column + "\n")
                for row in job.result():
                    df = pd.DataFrame([row])
                    df.to_csv(f, index=False, sep=",", header=False)
                    print(tabulate(df, headers='columns', tablefmt='psql'))
            elif format == 'tab':
                f.write(column + "\n")
                for row in job.result():
                    df = pd.DataFrame([row])
                    df.to_latex(f, index=False, header=False)
                    print(tabulate(df, headers='columns', tablefmt='psql'))
            else:
                raise Exception('For --out_file param please use one of next types: csv or tab, tab is deafult')


if __name__ == '__main__':
    db_connect()
