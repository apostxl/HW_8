from datetime import datetime, timedelta
from collections import defaultdict

from users import create_content
from faker import Faker


def get_next_week(d: datetime):
    diff_days = 7 - d.weekday()
    return d + timedelta(days=diff_days)


def prepare_birthday(text: str):
    bd = datetime.strptime(text, '%Y-%m-%d')
    try:
        return bd.replace(year=datetime.today().year).date()
    except ValueError:
        return bd.replace(year=datetime.today().year, month=3, day=1).date


def get_birthdays_per_week(users: list):
    birthdays = defaultdict(list)

    today = datetime.today().date()

    next_week_start = get_next_week(today)

    start_period = next_week_start - timedelta(2)
    end_period = next_week_start + timedelta(4)

    birthday_people = [
        user for user in users if start_period <= prepare_birthday(user['birthday']) <= end_period]

    if birthday_people:
        for user in birthday_people:
            current_bd = prepare_birthday(user['birthday'])

            if current_bd.weekday() in (5, 6):
                birthdays['0Monday'].append(user['name'])

            else:
                birthdays[str(current_bd.weekday())+current_bd.strftime('%A')
                          ].append(user['name'])

        return birthdays

    else:
        return None


def print_birthday_people(birthdays: dict):
    if birthdays:
        lst = []
        for key, value in birthdays.items():
            lst.append(f'{key}: {", ".join(value)}')

        lst = sorted(lst)
        sorted_lst = []

        for line in lst:
            for i in range(5):
                line = line.replace(str(i), '')
            sorted_lst.append(line)

        for line in sorted_lst:
            print(line)

    else:
        print("This week there don't be any birthdays.")


if __name__ == '__main__':
    user_input = int(
        input('Enter the number of employees in your fake company >>> '))

    print_birthday_people(get_birthdays_per_week(create_content(user_input)))


def create_content(count: int) -> list:
    fake = Faker()
    content = [{'name': fake.name(), 'birthday': fake.date()}
               for _ in range(count)]
    return content
