SERVICES = {
    "nginx":
        {
            "port": 25684,
            "start": ["nginx", "-c", "{project_dir}/nginx.conf"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
            "templates": ["nginx.conf.template"],
        },
    "gunicorn":
        {
            "port": 14449,
            "before": ["./before_deploy.sh"],
            "start": ["gunicorn", "-D", "-c", "settings_gunicorn.py", "{{ project_name }}.wsgi:application"],
            "after": ["./after_deploy.sh"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
}

