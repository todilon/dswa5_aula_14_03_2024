# Importa as bibliotecas necessárias do Flask e suas extensões
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_moment import Moment

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configura uma chave secreta para proteger os dados da aplicação
app.config['SECRET_KEY'] = 'hard to guess string'

# Inicializa as extensões Flask-Bootstrap e Flask-Moment
bootstrap = Bootstrap(app)
moment = Moment(app)

# Define uma classe de formulário Flask-WTF para a página de formulário
class NameForm(FlaskForm):
    name = StringField('Informe o seu nome', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    discipline = SelectField(u'Informe a sua disciplina:', choices=[('dswa5', 'DSWA5'), ('dwba4', 'DWBA4'), ('GPSA5', 'Gestão de projetos')])
    submit = SubmitField('Submit')

# Trata erros 404 (página não encontrada) redirecionando para uma página de erro personalizada
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Trata erros 500 (erro interno do servidor) redirecionando para uma página de erro personalizada
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Rota principal da aplicação, com métodos GET e POST permitidos
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm() # Instancia um formulário da classe NameForm
    if form.validate_on_submit(): # Verifica se o formulário foi submetido e é válido
        old_name = session.get('name') # Obtém o nome armazenado na sessão
        if old_name is not None and old_name != form.name.data: # Verifica se houve alteração no nome
            flash('Você alterou o seu nome!') # Exibe uma mensagem flash
        # Armazena os dados do formulário na sessão
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['institution'] = form.institution.data
        session['discipline'] = form.discipline.data
        session['remote_addr'] = request.remote_addr; # Obtém o endereço IP do cliente
        session['host'] = request.host; # Obtém o host do cliente
        return redirect(url_for('index')) # Redireciona para a mesma página após a submissão do formulário

    # Renderiza o template index.html passando o formulário e os dados da sessão
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           surname=session.get('surname'),
                           institution=session.get('institution'),
                           discipline=session.get('discipline'),
                           choices=dict(form.discipline.choices),
                           remote_addr=session.get('remote_addr'),
                           remote_host=session.get('host'),
                           current_time=datetime.utcnow()) # Passa o tempo atual para o template
