from app import create_app, Config, db

from app.models import User, Role, Visit, ScheduleTime, Permission


app = create_app(Config)
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Visit=Visit, ScheduleTime=ScheduleTime, Permission=Permission)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')