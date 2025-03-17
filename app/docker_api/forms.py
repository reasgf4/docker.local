from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, ValidationError
import re

class ContainerForm(FlaskForm):
    name = StringField('Container Name', validators=[DataRequired(), Length(min=1, max=64)])
    image = SelectField('Image', validators=[DataRequired()])
    ports = StringField('Port Mappings (e.g., 8080:80,8443:443)', validators=[Optional()])
    environment = TextAreaField('Environment Variables (e.g., KEY1=value1,KEY2=value2)', validators=[Optional()])
    submit = SubmitField('Create Container')
    
    def validate_name(self, name):
        if not re.match(r'^[a-zA-Z0-9_.-]+$', name.data):
            raise ValidationError('Container name can only contain letters, numbers, underscores, dots, and hyphens.')
    
    def validate_ports(self, ports):
        if ports.data:
            port_mappings = ports.data.split(',')
            for mapping in port_mappings:
                mapping = mapping.strip()
                if not re.match(r'^\d+:\d+$', mapping):
                    raise ValidationError('Port mappings must be in the format "host_port:container_port".')
    
    def validate_environment(self, environment):
        if environment.data:
            env_vars = environment.data.split(',')
            for env_var in env_vars:
                env_var = env_var.strip()
                if not re.match(r'^[a-zA-Z0-9_]+=.+$', env_var):
                    raise ValidationError('Environment variables must be in the format "KEY=value".') 