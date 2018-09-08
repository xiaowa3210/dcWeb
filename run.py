from flask_login import LoginManager

from app import app
from app.newmodels import User, db, Role, Permission

from backapp.backstage.main import main as main_blueprint

app.register_blueprint(main_blueprint)

from backapp.backstage.auth  import auth as auth_blueprint

app.register_blueprint(auth_blueprint)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

login_manager.init_app(app)

# from app.models import SuperAdmin
# db.app = app
#
# per =Permission('111','222')
# role = Role()
# role.roleName='admin'
# role.permissions =[per]
# per.roles=[role]
# admin = User(username='admin',password='admin')
#
# #
# admin.roles =[role]
# db.session.add(admin)
# db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.run(debug = True)
