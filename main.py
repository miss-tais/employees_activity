from getpass import getpass
from argparse import ArgumentParser
from datetime import datetime, timedelta


from employees_activity.hubstaff import HubstaffAuth, HubstaffAPI
from employees_activity.output_broker import OutputBroker


class EmployeesActivity(object):
    """
    Employees activity
    """
    def process_table_data(self, users_data):
        table_data = {
            'rows': [],
            'columns': [],
            'data': []
        }

        num_of_users = len(users_data)
        processed_projects = {}
        last_project_inx = 0

        for inx, user in enumerate(users_data):
            table_data['columns'].append(user['name'])

            for proj in user['projects']:
                if proj['id'] not in processed_projects:
                    table_data['rows'].append(proj['name'])

                    processed_projects[proj['id']] = last_project_inx
                    last_project_inx += 1

                    table_data['data'].append([''] * num_of_users)

                table_data['data'][processed_projects[proj['id']]][inx] = str(timedelta(seconds=proj['duration']))

        return table_data

    def process_employees_activity(self, output_mode, **kwargs):
        date = kwargs.get('date', (datetime.today() - timedelta(1)).date())
        user_email = kwargs.get('email', '')
        user_password = kwargs.get('password', '')
        organization_id = kwargs.get('organization_id', '')
        manager_email = kwargs.get('manager_email', '')

        hubstaff_auth = HubstaffAuth()
        auth_token = hubstaff_auth.auth(user_email, user_password)

        hubstaff_api = HubstaffAPI(auth_token)
        additional_filtering = {}
        if organization_id:
            additional_filtering['organizations'] = [organization_id]
        employees_activity_data = hubstaff_api.fetch_custom_team_report_by_date(date, date, **additional_filtering)

        organization = employees_activity_data['organizations'][0]
        table_data = self.process_table_data(organization['dates'][0]['users'])

        output = OutputBroker(organization['name'], date, table_data)
        if output_mode == 'email':
            output.send_table_as_email(manager_email)
        else:
            output.send_table_as_html()


if __name__ == '__main__':
    default_date = (datetime.today() - timedelta(1)).date().strftime("%Y-%m-%d")

    output_types = ['html', 'email']

    parser = ArgumentParser()
    parser.add_argument("-d", "--date", help="Employees activity date", default=default_date)
    parser.add_argument("-m", "--mode", help="Output mode", default='html')
    args = parser.parse_args()

    if args.mode not in output_types:
        output_mode = None
        print 'Wrong output mode'
    else:
        output_mode = args.mode

    try:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        date = None
        print 'Wrong date'

    if date and output_mode:
        manager_email = ''

        email_input_text = "User email: "
        password_input_text = "User password: "
        organization_id_input_text = "Organization id: "
        manager_email_input_text = "Manager email: "

        email = raw_input(email_input_text)
        while True:
            if email:
                break
            else:
                print 'Please enter email'
                email = raw_input(email_input_text)

        password = getpass(prompt=password_input_text)
        while True:
            if password:
                break
            else:
                print 'Please enter password'
                email = raw_input(password_input_text)

        organization_id = raw_input(organization_id_input_text)
        while True:
            if organization_id:
                break
            else:
                print 'Please enter organization id'
                organization_id = raw_input(organization_id_input_text)

        if output_mode == 'email':
            manager_email = raw_input(manager_email_input_text)
            while True:
                if manager_email:
                    break
                else:
                    print 'Please enter manager email'
                    manager_email = raw_input(manager_email_input_text)

        employees_activity = EmployeesActivity()
        employees_activity.process_employees_activity(output_mode,
                                                      date=date,
                                                      email=email,
                                                      password=password,
                                                      organization_id=organization_id,
                                                      manager_email=manager_email)