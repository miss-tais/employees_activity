import os

from jinja2 import FileSystemLoader, Environment

from employees_activity.settings import settings_loader


class OutputBroker(object):
    """
    Output broker.
    :param organization_name: Organization name
    :param date: Report date
    :param table_date: Report table data. Structure: {'rows': [], 'columns': [], 'data': [[], ]}
    """

    def __init__(self, organization_name, date, table_data):
        self.organization_name = organization_name
        self.date = date
        self.table_data = table_data
        file_path = os.path.abspath(os.path.dirname(__file__))
        self.jinja2_env = Environment(loader=FileSystemLoader(os.path.join(file_path, 'templates')), trim_blocks=True)

    def render_template(self, template_name):
        """
        Template rendering
        """
        template = self.jinja2_env.get_template(template_name)
        context = {
            'organization': self.organization_name,
            'date': self.date,
        }
        context.update(self.table_data)
        rendered_template = template.render(**context)
        return rendered_template

    def send_table_as_html(self):
        """
        Report rendering and saving to html file
        """
        rendered_template = self.render_template('index.html')

        file_name = "{file_name}.html".format(file_name=settings_loader.file_name.format(date=self.date))

        with open(os.path.join(settings_loader.file_path, file_name), "wb") as f:
            f.write(rendered_template)

    def send_table_as_email(self, email):
        rendered_template = self.render_template('activities_table.html')
        # TODO: implement emailing table to manager
