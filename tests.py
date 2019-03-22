from datetime import datetime

from employees_activity.output_broker import OutputBroker
from main import EmployeesActivity

user_data = {
    'organizations': [{
        'dates': [{
            'date': '2019-03-22',
            'users': [{
                'id': 1,
                'projects': [{
                    'duration': 13379,
                    'id': 1,
                    'name': 'hubstaff bot1'
                },
                    {
                        'duration': 1335,
                        'id': 3,
                        'name': 'hubstaff bot3'
                    }
                ],
                'name': 'user1'
            },{
                'id': 2,
                'projects': [{
                    'duration': 16569,
                    'id': 2,
                    'name': 'hubstaff bot2'
                },
                    {
                        'duration': 46526,
                        'id': 3,
                        'name': 'hubstaff bot3'
                    }
                ],
                'name': 'user2'
            },{
                'id': 2,
                'projects': [{
                    'duration': 55569,
                    'id': 4,
                    'name': 'hubstaff bot4'
                },
                    {
                        'duration': 13445,
                        'id': 1,
                        'name': 'hubstaff bot1'
                    }
                ],
                'name': 'user2'
            }]
        }],
        'id': 153487,
        'name': 'rt-bot-23'
    }]
}

if __name__ == '__main__':
    data = EmployeesActivity().process_table_data(user_data['organizations'][0]['dates'][0]['users'])
    OutputBroker('test organization', datetime.today().date(), data).send_table_as_html()
