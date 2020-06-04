from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


# description of SQL table
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# handle of database connection
session = Session()


def read_today_data_row():
    today = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline == today).all()

    print(f'Today {today.day} {today.strftime("%b")}:')

    if not rows:
        # No to-do in database
        print('Nothing to do!\n')
    else:
        # we have to-do in database
        for idx, data_row in enumerate(rows, 1):
            print(f'{idx}. {data_row.task}')

        print()
    return


def read_week_data_row():
    for offset in range(7):

        cur_day = datetime.today().date() + timedelta(days=offset)
        rows = session.query(Table).filter(Table.deadline == cur_day).all()

        print(f'{cur_day.strftime("%A")} {cur_day.day} {cur_day.strftime("%b")}:')

        if not rows:
            # No to-do in database
            print('Nothing to do!\n')
        else:
            # we have to-do in database
            for idx, data_row in enumerate(rows, 1):
                print(f'{idx}. {data_row.task}')

            print()

    return


def read_all_data_row():
    rows = session.query(Table).all()

    print('All tasks:')

    if not rows:
        # No to-do in database
        print('Nothing to do!\n')
    else:
        # we have to-do in database
        for idx, data_row in enumerate(rows, 1):
            print(f'{idx}. {data_row.task}. {data_row.deadline.day} {data_row.deadline.strftime("%b")}')

        print()
    return


def add_data_row():
    print('Enter task')
    content = input()
    print('Enter deadline')
    date_string = input()
    deadline_datetime = datetime.strptime(date_string, '%Y-%m-%d')
    new_row = Table(task=content, deadline=deadline_datetime)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')

def missed_tasks():
    rows=session.query(Table).filter(Table.deadline<datetime.today().date()).order_by(Table.deadline).all()
    for idx,row in enumerate(rows,1):
        print(f"{idx}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")

def delete_task():
    print("choose the number of the task you want to delete")
    rows=session.query(Table).order_by(Table.deadline).all()
    for idx,row in enumerate(rows,1):
        print(f"{idx}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    i=int(input())
    session.delete(rows[i])
    session.commit()
    print("The task has been deleted!")
while True:

    menu = '''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete Task
0) Exit'''

    print(menu)

    choice = int(input())

    if choice == 0:
        break

    elif choice == 1:
        # read today's task
        read_today_data_row()

    elif choice == 2:
        # read this week's task
        read_week_data_row()

    elif choice == 3:
        # read all task
        read_all_data_row()
    elif choice == 4:
        #Missed tasks
        missed_tasks()
    elif choice == 5:
        # add task
        add_data_row()
    elif choice == 6:
        #delete task
        delete_task()

print('Bye!')
