from wtforms import Form
from wtforms import TextField
from wtforms import validators
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField


class Formulario(Form):
    """docstring for Formulario"""
    username = TextField('Usuario', [validators.length(
        min=8, max=25, message="ingrese un usuario valido"),
        validators.required(message='el campo es requerido')]
    )
    password = PasswordField('Password', [validators.length(
        min=8, max=25, message="ingrese una pasword valida"),
        validators.required(message='el campo es requerido')]
    )
    email = EmailField('Correo electronico', [validators.required(
        message="el correo es requerido")]
    )
    nombre = TextField('nombre', [validators.length(
        min=3, max=20, message="ingrese un nombre valido")])
    cedula = TextField('Cedula', [validators.length(
        min=6, max=12, message="ingrese una cedula valida")])


class loggin(Form):
    """docstring for loggin"""
    username = TextField('Usuario',
                         [validators.length(min=8, max=25),
                          validators.required(message='el usuario es requerido')
                        ])
    password = PasswordField('Password', [validators.length(min=8, max=95),
                            validators.required(message="el usuario es requerido")])
