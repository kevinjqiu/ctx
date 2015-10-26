from ctx.server import app


if __name__ == '__main__':
    ctx_app = app.create_app()
    ctx_app.run(debug=True, host='0.0.0.0', port=8080)
